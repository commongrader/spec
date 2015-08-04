[**CommonGrader spec**] · [Readme](<README.md>) · **API** ·
[Libraries](<libraries.md>)

CommonGrader API
================

The CommonGrader API revolves around three classes of objects: graders,
submissions, and results. They will be lowercased and unstylized unless they are
implementation-specific.

Terminology and serialization
-----------------------------

Each CommonGrader type is defined as a hash-like data structure that consists of
**fields**. Field name are always strings, and the type of the value is
specified. Fields that take a list can also take in a string; it will be
converted to a one-element list. When serialized, fields should be always
lowercase.

A field name followed by a \* means the field is required; all other fields are
optional. The following values are always equivalent and will be referred to as
null: a missing value (in YAML), `null`, `None`, `nil`. A missing field is also
equivalent to these, except when applying inheritance (see
Assignments:Inheritance bellow). Whether JavaScript's `undefined` is treated as
null value or a missing field is, ironically, undefined for now.

Some objects may reference other CommonGrader objects. These can either be
serialized to/from the name of the referent, or its contents. Dates and times
should serialized to either seconds since Epoch or \_\_\_\_.

TODO: choose string date format

Graders
-------

A grader is a program or service that takes in submissions and outputs results.
Graders have the following properties:

| field    | type   | description                  |
|----------|--------|------------------------------|
| `name`\* | string | a way to identify the grader |

Graders invocation is language-specific, so CommonGrader stays away from
describing too much about them. However, graders can take in options and
assignments help organize those options.

Assignments
-----------

Assignments help provide parameters to graders, if desired. Assignments have the
following properties:

| field               | type            | description                                                                                   |
|---------------------|-----------------|-----------------------------------------------------------------------------------------------|
| `name`\*            | string          | a way to identify the assignment                                                              |
| `type`\*            | string          | a way to identify the type of assignment, intended to be used to select an appropriate grader |
| `expect`            | expecatations{} | a hash of expectations                                                                        |
| `​expect:input`      | expectations    | requirements for submissions to the grader                                                    |
| `expect:output`     | expectations    | guarantees for graded submissions from the grader                                             |
| `​expect:assignment` | expectations    | requirements for sub-assignments                                                              |

### Expectations

An expectations object is a string:boolean hash. Each key names a field name (of
the submission/result) and the boolean value specifies whether that field is
required to be present (true) or not present (false). The special `*` key
applies a requirement to the all properties not mentioned in this spec or in the
other keys.

### Inheritance

Why are graders and assignments not part of the same object?

-   Some grading systems use only one codebase to grade multiple assignments.

-   Some grading systems have different grading environments (autograde vs final
    submission) that will cause the same real assignment to be graded
    differently.

Graders are implementation-specific, so grader inheritance is undefined.
However, assignments are simple hashes, which makes inheritance a lot easier.

Assignments have the following inheritance-related properties:

| field  | type         | description                                                                                                                                                                                                                                                                               |
|--------|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `self​` | hash         | a hash of properties of the assignment itself, i.e., before inheritance is applied. *This property is guaranteed and is always auto-generated. It should never be explicitly given. Naive implementations may wish to set this to the keyword-argument hash that created the assignment.* |
| `base` | assignment[] | a list of assignments to inherit from. The properties from each super-assignment will be applied in this order. The current assignment can be specified with `self`, which will be automatically inserted last if not specified.                                                          |

Inheritance rules:

-   Fields are applied in order by merging fields from assignments in the order
    specified under `base`.

-   If a super-assignment has its own super-assignments, merge those first.

-   A null-like value means to not merge that field, i.e., it does not have
    special meaning to the hash-merge operation. However, this does make it
    special under CommonGrader, where null-like values in most situations act
    the same as missing fields.

-   If a list contains null, the null will be discarded and the new list will be
    merged instead of overwritten, by splicing the old list at the position of
    the null. Example: `[1, 2] + [3, null, 4] => [3, 1, 2, 4]`

-   If a hash has key that is the empty string, that entry will be discareded,
    and the hash will be merged instead of overwritten. The empty string instead
    of null is used because some languages (JavaScript) require keys to be
    strings.

-   `name`, `self`, and `base` have special meanings under inheritance and are
    excluded from inheritance rules. (Actually, `self` probably shouldn't even
    exist until after merging is complete.)

### Example

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
assignments:

 # This first assignment specifies srequirement for the grader
 - name: com.example.grader.cmd
   type: com.example.grader.cmd
   expect:
    - assignment:
        command: true
        # not required, but good way to self-document an optional property
        env: null
        *: false
    - input:
        files: true
    - output:
        exit-code: true

 - name: com.example.grader.cmd.submit-grades
   env:
     '': # enables merging this hash
     SUBMIT_GRADES: 1

 - name: com.example.cs101.hw1
   base: com.example.grader.cmd
   command: /usr/share/grader/bin/hw1

 - name: com.example.cs101.hw1
   base: com.example.grader.cmd, com.example.grader.cmd.submit-grades

 - name: com.example.cs101.hw2
   base: com.example.grader.cmd
   command: /usr/share/grader/bin/hw2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

That was a mouthful. Unfortunately, the inheritance system for submissions is a
little more complicated! :(

Just kidding. Unlike assignments, submissions and results aren't generated by
hand so they don't have inheritance. *Yay!*

Submissions
-----------

| field            | type         | description                                                        |
|------------------|--------------|--------------------------------------------------------------------|
| `name​​`           | any          | a way to identify the assignment                                   |
| `assignment`\*   | assignment[] | the assignment(s) to use for grading                               |
| `user​`           | any          | a way to identify the user/student whom this submission belongs to |
| `time​​​​​`           | time{}       | a hash of various times related to the submission                  |
| `time​:submitted` | time         | when the submission left the students control                      |
| `time:graded`    | time         | when the submission finished grading                               |

Graded submission
-----------------

This could be the same object as the submission but it doesn't have to be.

-   Some grading models treat the submission as read-only, returning a "results"
    object. Advantage: the submission can be re-used for grading via other
    methods.

-   Some grading models mutate the original submission. Advantage: No need to
    keep multiple objects around, can pass this through multiple graders that
    each add on their own results, then through a final grader that combines the
    results of the different graders.

CommonGrader works well with both systems.

| field          | type         | description                                                     |
|----------------|--------------|-----------------------------------------------------------------|
| `name​​`         | any          | a way to identify the assignment                                |
| `submission`   | submission   | the submission that this result is for                          |
| `assignment`\* | assignment[] | the assignment that produced this result                        |
| `grader`\*     | grader[]     | the graders that this submission passed through                 |
| `time`         | time{}       | (same as above)                                                 |
| `results​`\*    | any          | scores, breakdown of scores, you name it                        |
| `log​`          | any          | debug info produced by the grader that is meant to be persisted |
| `debug`        | any          | debug info produced by the grader that can be discarded         |
