# Angular

Angular - Plataform for building single-page client applications with HTML and Typescript

## Fundamental Concepts

Angular Componenents are organized into NgModules;
An angular app is a set of NgModules;
An app has a root module;
Views are sets of screen elements that Angular can choose among and modify according to program logic;
Services provide specific functionality not directly related to views;
Modules, componenets and services are classes that use decorators;
Decorators mark class type and provide metadata that tells angular how to use them;
Metadata for a component class associates it with a template that defines a view;
A template combines ordinary HTML with Angular directives and binding markups, allowing angular to modify HTML before renderization

## Modules

Declares compilation context for a set of componenets that is dedicated to an application domain, workflow or set of capabilities;
Can relate its componenets with code, such as services, to form functional units;
Modules can import functionality from other modules;

## Components

The root componenent connects a componenent hierarchy with the DOM;
Each componenet defines a class that contains application data and logic, associated with an HTML template that defines a view to be displayed in a target environment;


## Templates

Combine HTML and Angular markup which modify HTML elements before displayed.

## Data binding

Event binding responds to user input;
Property Binding interpolate values that are computed from application data into HTML;

