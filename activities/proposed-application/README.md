# Proposed Application: [CashierQ]

| | |
|---|---|
| **Student name** | Fernan, Pauline |
| **Section** | CS3B |
| **GitHub username** | paulinefernan0901-dotcom |
| **Date submitted** | 2026-10-23

---

## 1. Problem Statement

Students who need to pay at the cashier, especially during enrollment week, has to wait in long, crowded lines with no way of knowing when it will be their turn. This causes the office to be crowded and wastes time that students need for other enrollment steps.

### 1.1 Background

This problem happens in the cashier office as payment process has to be through that office. As for who experiences it, it applies to everyone who needs to undergo payments inside the school campus but I observed that the problem surges during enrollment week. This is because students would request documents in the registrar needed for enrollment and have to pay the cashier the amount needed for the request before the registrar would process it. I personally did come across this problem as I requested some documents for my scholarship during enrollment week and the line/queue was long when I had to go to the cashier office for the payment process.

### 1.2 Evidence from research

| Method | Who / where | Key finding |
|---|---|---|
| Interview | 3rd-year student who paid for a scholarship document during enrollment week | Only one cashier was working, so the line was long and the wait was much longer than expected. |
| Observation | Cashier office, enrollment week | Students waited on a bench at the side of the office while the cashier finished serving one student at a time. When the bench was full, others had to wait outside and could only come in as seats opened up. |
| Document review | Physical queue number handed to students when they entered the office | The office already used a paper queue number to manage the crowd, but it only worked once a student was inside, so people waiting outside had no number and no idea how long they would wait.|

| Method | Who / where | Key finding |
|---|---|---|
| Interview | 3rd-year student who requested a COR from the registrar for her stipend and had to pay the cashier first | The registrar would not process her request until she paid, and she had no way of knowing when her turn would come. |
| Observation | Cashier office during enrollment week | The line was long because many other students were also requesting a COR for their own stipends, and only one cashier was working. |
| Document review | There wasn't any queue tickets or numbers | The office had no queue tickets or numbers, so students had to stay in line until it was their turn.|

### 1.3 Point-of-view (POV) statement

Students who need to pay at the cashier, especially during enrollment week, need a way to know when their turn is coming while they do other things, because payment is one of the process they need to take to finish what they requested in the registrar, and time spent standing in the line can affect their time when they needed to finish other task.

### 1.4 "How might we…?" question

"How might we help students who pay at the cashier know when it’s their turn, without having to stand in a long line?"

### 1.5 Self-check

- [/] Names a real user group
- [/] States a need, not a feature
- [/] Rests on an insight from research
- [/] Is narrow enough to act on and open enough to allow different ideas

---

## 2. Target-User Profile

### 2.1 Primary persona

| | |
|---|---|
| **Name, age** | Dona, 21 |
| **Role / background** | 3rd-year student, College of Science and Mathematics |
| **Goals** | Pay for her requested documents quickly so the registrar can process them before her scholarship and enrollemt |
| **Frustrations / pain points** | Because it was enrollment week, the cashier was busy accommodating other students, leading to a long line. She had to wait longer than she anticipated. |
| **Context of use** | Uses a smartphone on campus Wi-Fi or mobile data; mostly during enrollment week, between classes or while visiting the registrar and cashier offices |
| **Accessibility considerations** | Needs large, readable queue numbers and simple text; the system should work on low bandwidth since campus connectivity can be unreliable |
| **Current workaround** | Arrives early and stands in line, or leaves and returns later hoping the line is shorter, risking a missed turn and a delayed registrar request |

### 2.2 User groups and stakeholders

| Group | Who | Relationship to the app |
|---|---|---|
| Primary users | Students who need to pay at the cashier (especially during enrollment week) | Use the app to get a queue number, see when their turn is coming, and avoid standing in a long line |
| Secondary users | Cashier staff and indirecly, the registrar staff | Cashier staff use the app to call the next number and manage the queue. While the app does not operate on the Registrar staff directly, they can still benefit from payments being processed in a more predictable order |
| Stakeholders | School administration| Approve and fund the system, maintain it, and are affected by crowding, processing times, and how smoothly enrollment runs throughout the week, or in cases where the cashier will be crowded by students for several payment reasons. |

### 2.3 Organizational needs

- **Data privacy:** Follow RA 10173 by collecting only what the queue needs (such as a student ID, email and the purpose of the process) and deleting the records aquired after a set time period.
- **Low cost and easy upkeep:** The system should be cheap to run and simple for cashier staff to use.
- **Reporting:** Admins need to know the busy hours and how long people wait, so they can plan how many staff to have during enrollment week.

---

## 3. Proposed Application

### 3.1 Concept

The CashierQ would be a queue app for the school cashier office. There will be instances where the line would be long, especially for enrollement week or incidents that require many students to request school documents at the same time. This can cause a long lines at the cashier office and and students don't know when their turn will come. With CashierQ, the students would join the queue on their phone, gets a ticket number, and can see how many people are ahead of them. With that, if their turn is still far from being called, they can deal with other important task while they wait and the app will inform them when its their turn. The cashier will also have a simple dashboard to call the next number and mark those who are done paying.

### 3.2 Value proposition

For **students who pay at the school cashier office** who **need to know when their turn will come without standing in a long line**, **VCashierQ** is a **queue web app** that **gives them a ticket number and shows how many people are ahead of them on their phone**. Unlike **the current line, where students just stay and wait**, it **tells them when they are called and lets the cashier call the next number with one click**.

| User side | Product side |
|---|---|
| **Goals:** Pay at the cashier, especially during enrollment week, to be able to finish the request from registrar, to pay any fees needed to be paid and to know when it's their turn. | **What the app does:** Join online and get a ticket, get a queue ticket for your number on what place you are at the waiting line |
| **Frustrations:** Standing in a long line with no idea how long it'll take, losing time while waiting, and afraid of missing their turn. | **How it fixes them:** No need to stand in line as there would be a feature in the app that shows "2 people ahead of you" to inform the user of their position of the queue. |
| **Benefits:** If their position of the line is very far, they would want to do other things that is needed to be done while waiting and still be able to come back later without having to take another line. | **How it helps:** There would be a ticket number given to the user after doing the join process in the app to help them track their position and when is the time they need to come back for their turn to help with their time effeciency. |

### 3.4 Existing applications (from your application analysis)

| Existing app | What it does well | Where it falls short | How your app differs |
|---|---|---|---|
| Qminder | Join by SMS, app or QR, also offers kiosk check-in | built for businesses in general, not a school cashier | Free and built around the school's own payment services |
| QLess | Remote queue joining and offer real-time wait updates, used by many universities | Built for large organizations so the the school would need to adopt it | Student-built, simple, and easy to change for the school's real needs |

### 3.5 Technology choice

**Options considered:** Mobile-friendly web app

**Weighted decision matrix** (scores 1–5, higher is better):

| Option | Solves the problem ×3 | Team skills ×2 | Cost ×2 | Privacy ×2 | Time to MVP ×1 | Total /50 |
|---|---|---|---|---|---|---|
| Mobile-friendly web app | 4 | 5 | 5 | 4 | 5 | 45 |
| Native mobile app | 5 | 2 | 3 | 3 | 2 | 33 |
| SMS-based queue | 4 | 3 | 2 | 3 | 3 | 31 |

**Chosen technology and rationale:** I chose the mobile-friendly web app as it solves the main problem, which is that students can't tell when their turn is coming while waiting for a long line during busy time for the cashier office. They can open a page on any phone, with nothing to install, and see their ticket and position. It's also the cheapest and fastest option in my opinion, and it needs only a name, student id, and email from students. So all in all, no emerging technology is needed when making the app.

---

## 4. Preliminary Requirements

### 4.1 Functional requirements (user stories)

| ID | User story | Priority (MoSCoW) |
|---|---|---|
| FR-01 | As a student waiting to pay, I want to join the queue with my name, student ID, email and the service I am paying for, so that I get a ticket number without standing in line. | Must |
| FR-02 | As a student waiting to pay, I want to see my ticket number and how many people are ahead of me, so that I know roughly when my turn will come. | Must |
| FR-03 | As a student waiting to pay, I want my status to update by itself, so that I know when I am called without refreshing the page. | Should |
| FR-04 | As a student waiting to pay, I want to leave the queue if I cannot wait, so that the cashier does not call a ticket nobody will answer. | Should |
| FR-05 | As a cashier, I want to see the waiting tickets in order, so that I know who is next. | Must |
| FR-06 | As a cashier, I want to call the next ticket with one click, so that students know whose turn it is instead of me just saying "next". | Must |
| FR-07 | As a cashier, I want to mark a ticket as served, so that finished students leave the list. | Must |
| FR-08 | As a cashier, I want to mark a ticket as a no-show, so that I can move on when nobody comes to the window. | Must |
| FR-09 | As a cashier, I want to see how many students are waiting for each service and filter the list by service, so that I can see the load at a glance. | Could |

### 4.2 Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | A student's ticket status and position update within 10 seconds of a cashier action, without reloading the page. Each page loads in under 3 seconds on a mobile connection. |
| NFR-02 | Usability | A first-time student can join the queue and find their ticket number in under 2 minutes without help. Pages work at 375 px wide with no sideways scrolling, and the main buttons are at least 44 px tall. |
| NFR-03 | Security / privacy | Student ID, name and email are only shown to the cashier and to the student who owns the ticket. The server validates every form field. Only the cashier can change a ticket's status, through POST requests. |
| NFR-04 | Compatibility | Works in current versions of Chrome or any websites on phones and on laptops, with no app install. |

### 4.3 MoSCoW summary

- **Must have:** FR-01 join the queue and get a ticket; FR-02 see ticket number and people ahead; FR-05 cashier sees the waiting list in order; FR-06 call next with one click; FR-07 mark served; FR-08 mark no-show.
- **Should have:** FR-03 status updates by itself; FR-04 student can leave the queue.
- **Could have:** FR-09 waiting count per service and filter by service.
- **Won't have (this time):** FR-10 cashier login; SMS or email alerts; native mobile app; payment inside the app.

---

## 5. Minimum Viable Product (MVP)

### 5.1 MVP features

1. **Join the queue online (FR-01):** A student fills in their name, student ID, email and what they're paying for, and gets a ticket number right away, with no need to line up first.
2. **See my ticket and place in line (FR-02):** The student sees their ticket number in big text, their status, and how many people are ahead of them, so they know roughly when to come back.
3. **Cashier sees the waiting list (FR-05):** The cashier gets one list of everyone waiting, in order, so there's no guessing who's next.
4. **Call the next student (FR-06):** One click calls the next ticket, so students know it's their turn and the cashier doesn't have to just say "next."
5. **Mark a ticket as served or no-show (FR-07, FR-08):** Finished students leave the list, and the cashier can move on when someone doesn't show up.

### 5.2 Out of scope

- **Cashier login (FR-10):** For now the staff page is open to anyone who knows the link. 
- **SMS or email alerts:** Students can only see the updates by keeping the page open, so sending messages can cost extra set up, which is out of scope or capabilities.
- **Native mobile app:** The web app already works on any phone, and building a separate app takes more time and skills to make it happen.
- **Paying inside the app:** The app only manages the line so the students should still have to pay at the cashier window.
- **Estimated waiting time:** The app will show how many people are ahead, but not how many minutes.
- **Real database storage:** Tickets are kept in memory for now, so it reset when the server restarts.

### 5.3 Constraints and assumptions

- **Constraints:** I have one semester to finish this, and I'm working alone. There's no budget, so I can only use free tools and hosting. Staff login and a real database aren't ready until later weeks. The app is built with Flask, HTML and Bootstrap because those are the skills taught in the course.
- **Assumptions:** Students have a smartphone or access to a laptop with internet. The cashier has a device with a browser at the window and will utilize the dashboard consistently as the app only works if every ticket is called, served or marked no-show. Students will give an email that actually works. 

### 5.4 Feasibility check (TELOS)

| Dimension | Key question | Your assessment |
|---|---|---|
| Technical | Can I build it with my skills and tools? | Yes. The MVP only needs Flask, HTML, Bootstrap and a little JavaScript, which we learned in class. I already have the join, ticket and staff screens working. |
| Economic | Do the benefits justify the costs? | Yes. It costs nothing to build and run because I only use free tools. The benefit is that students save time and the cashier gets a clearer list. |
| Legal | Does it comply with law and policy (e.g., RA 10173)? | Mostly. The app collects names, student IDs and emails, which are personal data under the Data Privacy Act (RA 10173). I only ask for what the queue needs, and only the student and the cashier see it. Before real use, the school would need a privacy notice and a way to delete old tickets. |
| Operational | Will people use it, and can it be run? | Probably. Students already use their phones all day, and the screens are simple. It only works if the cashier keeps the dashboard updated, so that needs to be tested with real staff. |
| Schedule | Can I deliver the MVP this semester? | Yes. The MVP is small, and the Week 3 screens already cover most of it. The database and login come in later weeks. |

**Verdict:** Feasible if the cashier is willing to use the dashboard during busy hours and a basic privacy notice is added before real students use it.

---

## Submission Checklist

- [/] File saved as `activities/proposed-application/README.md` in my CCC181 repository
- [/] All `[bracketed placeholders]` replaced and guidance blockquotes removed
- [/] Sections 1–5 complete
- [/] Images (if any) placed in `images/` and displaying correctly on GitHub

