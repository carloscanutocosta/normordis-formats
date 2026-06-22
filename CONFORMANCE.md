# Conformance

## Purpose

This document defines what it means for an implementation to claim conformance with NORMORDIS specifications.

## Principles

- Conformance is demonstrated through evidence.
- Specifications are normative; implementations are not.
- Passing a conformance suite does not transfer authority to an implementation.
- Claims of conformance must be version-specific.

## Roles

An implementation may conform in one or more roles:

- Producer
- Reader
- Renderer
- Validator

Conformance to one role does not imply conformance to another.

## Conformance Requirements

A conformant implementation shall:

- implement the normative behaviour of the specification;
- correctly process official conformance vectors;
- declare supported specification versions;
- identify its supported role(s).

## Conformance Suites

The project publishes official conformance suites containing:

- valid examples;
- invalid examples;
- edge cases;
- interoperability vectors;
- regression vectors.

## Conformance Declaration

A declaration should identify:

- specification;
- version;
- role;
- profile;
- conformance-suite version.

## Certification

The project does not currently provide formal certification.

Conformance claims remain the responsibility of the declaring party.