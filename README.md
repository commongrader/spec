[**CommonGrader spec**] · **Readme** · [API](<api.md>) ·
[Libraries](<libraries.md>)

CommonGrader
============

Computer science courses need customized autograder infrastructure. CommonGrader
can help.

What is CommonGrader?
---------------------

CommonGrader is a set of protocols and libraries that assist with development
efforts that are common to many autograder systems.

CommonGrader is a **spec** that describes:

-   A format for 3 common **objects** that autograders pass around.

-   A format for some common **tasks** that autograders do.

CommonGrader a collection of **code libraries** to do some CommonGrader things:

-   A **base library** for both Ruby and Python that includes support for
    CommonGrader objects. Note that the spec is still the primary document!

-   **Adapter libraries** to make the third-party services you use speak
    CommonGrader.

-   For really common tasks (e.g., autograder selection), a **library** that
    does that task.

Why CommonGrader?
-----------------

**Use only what you want.** Your stack can be converted to CommonGrader
piece-by-piece. Nothing needs to be changed about the components not converted
to CommonGrader, and it's totally fine to have an app that's only partially
CommonGrader.

**Works with your stack.** The CommonGrader spec isn't revolutionary – you're
probably already doing something very similar. In addition, the CommonGrader
protocol is concerned with what kind of information flows across the autograder
toolchain, not how it flows on an implementation level. You can still transfer
your information within Ruby, via HTTP, or through a command line, or be
event-driven or polling, CommonGrader doesn't care.

**Future-compatible.** CommonGrader-conforming components receive the benefit of
being compatible with other CommonGrader components. Switching to the most
popular new LMS in two years? If it's popular enough, someone may have already
beat you to writing that integration.

**Fun to use!** Adopting large frameworks is a pain. CommonGrader was designed
to be a very unopinionated yet useful framework, so you can receive benefits
every step of the way.

How to CommonGrader?
--------------------

CommonGrader is, among other things, a useful abstraction for thinking about
autograding workflows. For example, consider this one, put in terms of
CommonGrader objects:

![](<assets/flow-github-octobear.png>)

In this workflow, a student submits an assignment via GitHub, which sends a
notification (via webhook) to a custom app called Octobear. Even though Octobear
all runs on one machine, it's conceptually useful to break it down into parts.
Here, Octobear is also the autograder and the grade db, and so it grades the
submission and stores the resulting grade.

The blue parts are the things you don't have control over. CommonGrader can make
make the rest easier to manage:

-   No need to make your own Submission, Assignment, and Result classes. Just
    import/require the CommonGrader base library to make these classes –
    complete with de/serialization and validation – accessible to you instantly.

-   CommonGrader is a format for data exchange. All exchanges that take place
    over green arrows can use the CommonGrader format. There's no need to switch
    to CommonGrader immediately if you already have a working custom protocol!
    You can do it each time a component needs to be rewritten.

-   It turns out that the GitHub adapter, Octobear I, Octobear II are generic
    components that can be used by other autograder projects. These can be
    open-sourced and subject to peer review and improvement.

-   If you're just starting out, or if you decide to need to change your entire
    infrastructure, these three modularized components can be used as-is.

### Examples: Berkeley CS on CommonGrader

Following are some (approximations of) existing workflows, put in terms of
CommonGrader. As with above, green arrows represent data exchanges can be in
CommonGrader.

-   61B-Hug workflow (used in example above)

    ![](<assets/flow-github-octobear.png>)

-   61B-Hilfinger workflow for autograder emails

    ![](<assets/flow-gitolite-glookup-auto.png>)

-   61B-Hilfinger workflow for autograding for grades

    ![](<assets/flow-gitolite-glookup-record.png>)

-   169 workflow

    ![](<assets/flow-xqueue-rag.png>)

### Adapters

Most autograders use one or more external services, usually to store code (e.g.,
GitHub) or to post grades (e.g., some LMS). These services don't interface in
CommonGrader, and it's unlikely they will in the near future. The CommonGrader
project aims to provide an adapter library for each such case, to make sure that
translation code is kept to a minimum.

This is an example of an adapter.

![](<assets/adapter-full.png>)

In shorthand, it is expressed as:

![](<assets/adapter-short.png>)

Who is CommonGrader?
--------------------

CommonGrader was started as a collaboration among autograder development efforts
at UC Berkeley. [@szhu](<https://github.com/szhu>) currently maintains this
project.

CommonGrader can be you, too! CommonGrader strives to be a framework useful to
everyone working on autograders. If you have have suggestions that would make
CommonGrader more useful to you, please open an issue or submit a pull request.
