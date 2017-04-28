# HOWTOs

HOWTOs are documents that cover a single, specific topic,
and attempt to cover it fairly completely.

It's Modelled on the Linux Documentation Project's HOWTO collection, this collection is an effort to foster documentation that's more detailed & useful.

## Overview of a Simple File Transfer Workflow HOWTO

*Author:* Chris Falck

- TODO: Extend example

- topic::Abstract

   This document is an introductory tutorial to using xfero. It provides a simple overview.


##Introduction

This document details an overview of what xfero is doing to handle a simple File transfer workflow.

**Example Usage:**

1. Xfero Startup - Scheduler starts all scheduled tasks. Each task has a priority to enable transfers to be prioritised.

  For example a task with High priority will monitor files to transfer every 5 minutes, while a task with low will monitor files to transfer every 15 minutes. These settings are configurable and are supplied as an example only.

2. A File is transferred to system running xfero using a COTS Product/Protocol.

3. One of the scheduled tasks initiated in [1] will be a monitor process which picks up the file received and initiated the associated workflow. Workflow can
include any number of functions for example, file renaming, compression etc.

4. When workflow is complete the file transfer is initiated to one or more destinations.
