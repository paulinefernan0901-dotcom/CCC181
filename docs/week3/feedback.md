# Week 3 self-review: personas and wireframes

I reviewed the three screens at phone and laptop width against my two personas, Dona (the person waiting) and Teresa (the cashier), using the six review questions. Then, I updated the wireframes based on the changes I assessed:

## Join the queue

**Works well:** The form is short (name, student ID, email, one service dropdown), and the full-width "Get a ticket" button is easy to reach with one thumb on the phone. This follows my rule that Dona is in a hurry and holding things, so the form must be quick to finish.

**Problem:** The service names were not consistent across screens. Join, My place and the real service list each used different wording, so a student could not be sure which option matched what she was paying for and can cause confusion for them. This breaks the *consistency* and *match with the real world* principles.

**Change:** I made it so that the three services listed in the base.html matches on all wireframes:"Registrar document fees", "Tuition and other fees" and "Other payments". I dropped "Official receipt / refund", because a receipt is given after paying rather than queued for, and I could not confirm that students queue for refunds. The layout stays the same.

## My place

**Works well:** The ticket number is the biggest thing on the screen, with the service, status badge and "4 people ahead of you" directly under it. This follows *visibility of system status* and my rule that her number and position must be the first thing she sees when she views her screen.

**Problem:** The first version gave no sign that the page refreshes by itself, even though FR-03 says it must. Dona might keep reloading or wonder whether the information is old. This breaks *visibility of system status*. The "Leave the Queue" button is also one tap away, so an accidental tap would lose her place (*error prevention*).

**Change:** I added a statement that says "Updates automatically" line under the position text to inform the student that the position consistently updates as soon as the queue ahead of her is finished.I also did a changed "Leave the Queue" button to red so it reads as a risky action, kept it smaller than the ticket number, and will add a confirmation step before it submits eventually. All in all, both My place frames has many changes.

## Staff dashboard

**Works well:** The waiting counts per service let Teresa see the load at a glance, and the table lists tickets in order with the status of each. This follows *visibility of system status*.

**Problem:** In the first version "Call next" sat at the bottom, below the table, in grey. It is the action Teresa does most often and the placement and design made it less visible. This breaks my rule that Call next must be the easiest and biggest button.

**Change:** I moved "Call next number" above the table in green and renamed the columns to No., Name, Status, Service and Actions. The service filter is drawn as a text box, but I will build it as a dropdown of the three services. Both staff frames are updated. I also fixed the requirement IDs. The staff frames said FR-04, but FR-04 is the student leaving the queue, so they now list FR-05 (waiting list in order), FR-06 (call next), FR-07 (mark served), FR-08 (mark no-show) and FR-09 (waiting count per service and filter). The My place frames now list FR-04 too, because they have the Leave the Queue button. The persona lines on the laptop frames now name the right device.