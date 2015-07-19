[**CommonGrader spec**] · [Readme](<README.md>) · [API](<api.md>) ·
**Libraries**

CommonGrader Libraries
======================

No CommonGrader libraries exist yet, but expect the following soon:

| name             | py   | rb   | description                                                                                                                                                                                                  |
|------------------|------|------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `base`           | soon | soon | Provides the `Submission`, `Assignment`, and `Result` classes, with validation and common de/serialization methods.                                                                                          |
| `subq`           |      |      | Provides a local submission queue, appropriate for converting event-based submission pushes (i.e., GitHub) into a polling model. Also includes a method to start a webserver that supports queue operations. |
| `octosub`        | soon | soon | Listens for submissions from GitHub and passes them to a callback as a CommonGrader submission. Provides a method that launches a webserver that is suitable for a GitHub webhook.                           |
| `xqueuesub`      |      |      | Polls a edX XQueue and retrieves the next submission as a CommonGrader submission.                                                                                                                           |
| `local-dispatch` | soon |      | Given a submission and a set of assignments, launches the command-line autograder to grade that submission.                                                                                                  |
| `http-dispatch`  |      |      | Given a submission and a set of assignments, makes an HTTP request to an autograder service to grade that submission.                                                                                        |
