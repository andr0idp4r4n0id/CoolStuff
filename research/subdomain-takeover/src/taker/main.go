package main

import (
    "bufio"
    "encoding/json"
    "flag"
    "fmt"
    "io"
    "net"
    "net/http"
    "os"
    "regexp"
    "strings"
    "sync"
    "time"

    "github.com/buger/jsonparser"
    "github.com/jpillora/go-tld"
    "github.com/miekg/dns"
    probing "github.com/prometheus-community/pro-bing"
)

type Fingerprints struct {
    Fingerprint string `json: "fingerprint" `
    Vulnerable  bool   `json: "vulnerable"`
}

var checked_domains []string

func CheckDomainAvailability(domain string, cname string) bool {

    url := "https://www.whatsmydns.net/api/domain?q=" + strings.Trim(cname, " \n\r\t")
    req, err := http.NewRequest("GET", url, nil)
    if err == nil {
        res, err := http.DefaultClient.Do(req)
        if err == nil {
            defer res.Body.Close()
            body, err := io.ReadAll(res.Body)
            if err == nil {
                val, err := jsonparser.GetBoolean(body, "data", "registered")
                if !(val) && err == nil {
                    for _, dom := range checked_domains {
                        if dom == cname {
                            return false
                        }
                    }
                    checked_domains = append(checked_domains, cname)
                    fmt.Println("[DOMAIN] = " + cname + " AVAILABLE FOR AUCTION")
                    return true
                }
                val_s, err := jsonparser.GetString(body, "data", "expires")
                if (len(val_s)) > 0 && (err == nil) {
                    for _, dom := range checked_domains {
                        if dom == cname {
                            return false
                        }
                    }
                    checked_domains = append(checked_domains, cname)
                    t, err := time.Parse("2006-01-02T15:04:05.000000Z", val_s)
                    if err != nil {
                        fmt.Println(err)
                        return false
                    }
                    if int(time.Until(t).Hours()) <= 3720 {
                        fmt.Println("[DOMAIN] = " + domain + " EXPIRES IN " + time.Until(t).String() + "[CNAME/NS] = " + cname)
                        return true
                    }
                }
            }
        }
    }
    return false
}

func ReadFingerprints(fingerprint []Fingerprints) []Fingerprints {
    data, err := os.Open("fingerprints.json")
    if err != nil {
        fmt.Fprintln(os.Stderr, "fingerprints.json not found. Are you in the same directory?")
    }
    defer data.Close()
    bytes, _ := io.ReadAll(data)
    json.Unmarshal([]byte(bytes), &fingerprint)
    return fingerprint
}

func CheckVulnerableFingerprints(domain string, fingerprint []Fingerprints) bool {

    req, err := http.Get("http://" + domain)
    if err == nil {
        defer req.Body.Close()
        body, err := io.ReadAll(req.Body)
        if err == nil {
            for _, print := range fingerprint {
                if !print.Vulnerable {
                    continue
                }
                if len(print.Fingerprint) > 0 {
                    string_body := string(body)
                    string_body = strings.ToLower(strings.TrimSpace(string_body))
                    if strings.Contains(string_body, strings.ToLower(strings.TrimSpace(print.Fingerprint))) {
                        fmt.Println("[DOMAIN]:[FINGERPRINT] = " + domain + ":" + print.Fingerprint)
                        return true
                    }
                }
            }
        }
    }
    return false
}

func IsDeadCname(domain string, in *dns.Msg) {

    lowered_code := strings.ToLower(dns.RcodeToString[in.Rcode])
    if lowered_code == "nxdomain" {
        fmt.Println("[DOMAIN] " + domain + " = " + lowered_code + " [CNAME]")
    }
    if len(in.Answer) > 0 {
        u, _ := tld.Parse("https://" + strings.TrimSuffix(in.Answer[0].(*dns.CNAME).Target, "."))
        CheckDomainAvailability(domain, u.Domain+"."+u.TLD)
    }
}

func IsIpDead(domain string) {

    ips, err := net.LookupIP(domain)
    if err != nil {
        return
    }
    for _, ip := range ips {
        pinger, err := probing.NewPinger(ip.String())
        if err != nil {
            continue
        }
        pinger.Count = 2
        err = pinger.Run()
        if err != nil {
            continue
        }
        stats := pinger.Statistics()
        if int(stats.PacketLoss) == 100 {
            fmt.Println("[DOMAIN] IP might be available for registration: " + ip.String() + ":" + domain)
            continue
        }
    }
}

func ParseNameserver(ns string, domain string) bool {
    u, err := tld.Parse("https://" + strings.TrimSuffix(ns, "."))
    if err != nil {
        return false
    }
    if CheckDomainAvailability(domain, u.Domain+"."+u.TLD) {
        return true
    }
    return false
}

func CheckReturnCodeNS(domain string, in *dns.Msg, host string) {
    lowered_code := strings.ToLower(dns.RcodeToString[in.Rcode])
    if lowered_code == "servfail" || lowered_code == "refused" {
        fmt.Printf("[DOMAIN:NS] = %s:%s\n", domain, host)
        return
    }
}

func main() {
    // Check for stdin input
    stat, _ := os.Stdin.Stat()
    if (stat.Mode() & os.ModeCharDevice) != 0 {
        fmt.Fprintln(os.Stderr, "No domains detected: cat domains.txt | taker")
        os.Exit(1)
    }

    var conc = flag.Int("c", 2, "concurrency")
    re := regexp.MustCompile(`pdns.*\.ultradns.com|udns.*\.ultradns.com|sdns.*\.ultradns.com|ns-.*awsdns-.*\.org|ns-.*awsdns-.*\.co\.uk|ns-.*awsdns-.*\.com|ns-.*awsdns-.*\.net|ns1\.domainpeople\.com|ns2\.domainpeople\.com|a\.dns\.gandi\.net|b\.dns\.gandi\.net|c\.dns\.gandi\.net|ns1\.hover\.com|ns2\.hover\.com|ns1\.hostinger\.com|ns2\.hostinger\.com|ns1\.mediatemple\.net|ns2\.mediatemple\.net|.*\.namecheaphosting\.com|.*\.registrar-servers\.com|ns.*activision\.com|adobe-dns-0.*\.adobe\.com|.*\.ns\.apple\.com|ns.*automattic\.com|ns.*\.capitalone\.com|ns.*\.twdcns\.com|ns.*\.twdcns\.info|ns.*\.twdcns\.co\.uk|ns.*\.google\.com|authns.*\.lowes\.com|ns10\.tmobileus\.com|ns10\.tmobileus\.net`)
    var wg sync.WaitGroup
    workers := make(chan string)
    workers_2 := make(chan string)
    msg_channel := make(chan *dns.Msg)
    client := new(dns.Client)
    quit := make(chan bool)
    var fingerprint []Fingerprints
    fingerprint = ReadFingerprints(fingerprint)
    skip := make(chan bool)

    wg.Add(1)
    go func() {
        defer wg.Done()
        s := bufio.NewScanner(os.Stdin)
        for s.Scan() {
            workers <- s.Text()
        }
        quit <- true
        close(workers)
    }()

    wg.Add(1)
    go func() {
        defer wg.Done()
        s := bufio.NewScanner(os.Stdin)
        for s.Scan() {
            workers_2 <- s.Text()
        }
        quit <- true
        close(workers_2)
    }()

    for i := 0; i < *conc; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for domain := range workers {
                if CheckVulnerableFingerprints(domain, fingerprint) {
                    skip <- true
                    continue
                }
                msg := <-msg_channel
                msg.SetQuestion(dns.Fqdn(domain), dns.TypeCNAME)
                in, _, err := client.Exchange(msg, "1.1.1.1:53")
                if err != nil {
                    continue
                }
                IsDeadCname(domain, in)
                IsIpDead(domain)
            }
        }()
    }

    for i := 0; i < *conc; i++ {
        wg.Add(1)
        go func(re *regexp.Regexp) {
            defer wg.Done()
            for domain := range workers_2 {
                nss, err := net.LookupNS(domain)
                if err != nil {
                    skip <- true
                    continue
                }
                for _, ns := range nss {
                    if re.MatchString(ns.Host) {
                        skip <- true
                        continue
                    }
                    if ParseNameserver(ns.Host, domain) {
                        skip <- true
                        continue
                    }
                    msg := <-msg_channel
                    msg.SetQuestion(dns.Fqdn(domain), dns.TypeA)
                    in, _, err := client.Exchange(msg, ns.Host+":53")
                    if err != nil {
                        continue
                    }
                    CheckReturnCodeNS(domain, in, ns.Host)
                }
            }

        }(re)
    }
    wg.Add(1)
    go func() {
        defer wg.Done()
        for {
            select {
            case <-skip:
                continue
            case <-quit:
                return
            case msg_channel <- new(dns.Msg):
                continue
            }
        }
    }()
    wg.Wait()
    close(msg_channel)
}
