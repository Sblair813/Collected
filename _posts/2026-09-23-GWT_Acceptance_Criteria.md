---
layout: post
title: "How well written Acceptance Criteria can make all the difference"
date: 2026-09-23
---

During the pandemic, my team had the privilege of taking part in immersive Agile Dojo training. We were already a high-performing team, but wow, did our performance accelerate after Dojo!

By now, you've probably heard of Given-When-Then (GWT). If you aren't using this format yet, keep reading, because I'm going to convince you that you need to use it!

GWT not only gives developers a clear understanding of the work, it also gives QA a roadmap for testing. That is, if it's done well!

Once we adopted GWT, my team experienced:
* Well written, complete technical stories 
* A shared language across business, development, and QA
* Fewer bugs
* Less rework
* Fewer clarification questions from developers AND QA
* Faster QA sign-off
* Shorter Sprints (yes, we were able to move to a shorter sprint cycle)

It changed how I worked, too. Writing in GWT forced me to think through every technical story more thoroughly, and it eliminated miscommunication on my end. It helped me tell the complete story, not just part of it.

**GWT Broken Down**
* **GIVEN:** the context or initial state
* **WHEN:** the action, event, or trigger
* **THEN:** the expected result or outcome

Think of it this way: here's where we start, here's what happens, and here's what should happen as a result.

Here's a generic example for a Help Request module in an application.

NEW FUNCTIONALITY: Help Request
Scenario 1:
**GIVEN** I am logged into the Pack application

**WHEN** the home screen displays

**THEN** I see the New Request button


Scenario 2:
**GIVEN** I am on the New Request screen

**WHEN** I click the Reason drop-down

**THEN** I see the following options:

* Supplies
* Clean up/Item spilled
* Technical Support
* Login Errors

Scenario 3:
**GIVEN** I have selected a reason

**WHEN** I click Submit

**THEN** I see a confirmation message that my request was submitted






