## Dona, the person waiting

> "I only needed to pay for one document, but I waited in line much longer than I expected." *(interview)*

| | |
| --- | --- |
| **Photo or sketch** | ![Sketch of Dona, the student](images/Dona.png) |
| **Age, role and background** | 21 years old, a 3rd-year student from the College of Science and Mathematics. She is requesting documents from the registrar for her scholarship and enrollment. |
| **Goals** | To pay the cashier for her requested documents quickly so the registrar can process them. She also wants to know when her turn will come as well as get everything done before her next class and her enrollment deadlines. |
| **Frustrations** | During enrollment week the cashier is very busy, so the line is long and she waits much longer than she planned *(observation)*. The registrar won't process her request until she pays, so everything is stuck behind that line *(interview)*. She also can't leave the line, or she loses her place. |
| **Devices and context** | Uses her smartphone on campus, between classes or near the registrar and cashier offices. Her mobile data is often slow, or the campus Wi-Fi is. She is usually standing and holding other things. |
| **Tech comfort** | Medium. She uses her phone for school every day, but she wants screens that are simple and quick. |
| **Accessibility needs** | Often has one hand busy, so she needs big buttons and big numbers. Her connection is slow, so pages needs to load fast. She is also often outside in bright light, so the text needs to have a strong contrast. |

### Scenario

It's enrollment week. Dona just got her request slip from the registrar for a scholarship document, but the line at the cashier is long and she has to wait for a while due to it. She opens CashierQ on her phone, picks "Document request payment", and gets ticket #27. The app says 8 people are ahead of her, so she goes to buy lunch and checks the app now and then. When her status changes to "Called", she walks to the cashier, pays, and brings her receipt back to the registrar.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| Join the queue for a document request payment | Join | FR-01 |
| Check her ticket number and how many people are ahead | My place | FR-02 |
| Know when she is called without refreshing | My place | FR-03 |
| Leave the queue if she can't wait | My place | FR-04 |

### What this means for my interface

1. Dona checks her phone while standing or walking with one hand free, so her ticket number and position should be the biggest thing on My place.
2. Her mobile data is often slow, so pages should load fast and avoid big images.
3. She might be in walking around while waiting for her turn or at the registrar when she's called, so the status should change by itself without her refreshing.
4. Since she is busy around that time, the Join form should be short: name, student ID, email and one service choice.


## Teresa, the staff member


| | |
| --- | --- |
| **Photo or sketch** | ![Sketch of Teresa, the cashier](images/Teresa.png) |
| **Age, role and background** | 45 years old, a cashier at the school cashier office. She handles payments for registrar documents, tuition and other fees, and also other payments that is handled by the school cashier office. |
| **Goals** | To serve students one at a time and make it clear who is next. She wants to keep the line moving during enrollment week, and to see right away how many students are still waiting. |
| **Frustrations** | During enrollment week the line is long and each payment takes time. Additionally, since there are many students requesting on the registrar office every enrollment week, the line continuously fill up. As for how she handles the queue, she just says "next," and just leave it to the students to decide who to come next based on the line they lined up to. When someone doesn't show up, she has to wait and guess if the student left or just didn't hear her. |
| **Devices and context** | Uses a shared desktop or laptop at the cashier counter. Students are always waiting at the window while she works, so she needs to do things fast, with one click. |
| **Tech comfort** | Medium. She uses the school's payment system every day, but she likes simple screens that don't need a lot of clicks. |
| **Accessibility needs** | The office PC is shared, so she should be able to start right away with no login or setup. The counter is busy, so she needs big, clearly labeled buttons that are hard to click by mistake. The office is brightly lit, so the text needs strong contrast. |

### Scenario

It's enrollment week and the line is already long when Teresa opens CashierQ on the counter computer. The dashboard shows the waiting students in order, so she presses "Call next" and ticket #12 is shown in big numbers. Instead of just saying "next," she says "Number 12," and the right student walks up. The student pays, and she marks the ticket as served. A few tickets later she calls #15, but nobody comes to the window. She marks it as no-show and moves on to the next person without losing her pace.

### Top tasks in the app

| Task | Screen | Requirement ID |
| --- | --- | --- |
| See the waiting list in order | Staff dashboard | FR-05 |
| Call the next student | Staff dashboard | FR-06 |
| Mark a student as served | Staff dashboard | FR-07 |
| Mark a student as no-show | Staff dashboard | FR-08 |
| Filter the list by service | Staff dashboard | FR-09 |

### What this means for my interface

1. Teresa deals with a long line all day, so "Call next" should be the easiest and biggest button on the dashboard.
2. Students get confused when she only says "next," so the ticket being called should show in big numbers, so she can say the number out loud and students can see it too.
3. She handles students quickly and a wrong click could skip someone, so Serve and No-show should be separate, clearly labeled buttons that show the ticket number.
4. She works on a shared office computer, so the dashboard should work right away with no setup, and the waiting list should be easy to read from a distance.