### 1a. Describe your setting and the problem

# CashierQ requirements

**Setting:** School cashier office, busiest during enrollment week

**People who wait:** Students paying for registrar documents, tuition and other fees, or other payments, such as Dona ([personas](week3/personas.md))

**People who serve:** Cashier staff at the counter, such as Teresa ([personas](week3/personas.md))

**Problem statement:** A student who needs to pay at the cashier needs a way to know when it is their turn without standing in line, because they lose their place whenever they step away and the registrar will not process their request until they have paid.

### 1b. Functional requirements

| ID | Requirement | Priority | Stores data? | Status |
| --- | --- | --- | --- | --- |
| FR-01 | A student can join the queue by entering their name, student ID, email and the service they are paying for, in under 30 seconds. | Must | **Yes** | Built (Week 3) |
| FR-02 | A student can see their ticket number and how many people are ahead of them. | Must | **Yes** | Built (Week 3) |
| FR-03 | A student can see their status change to "Called" without refreshing the page. | Should | No | Built (Week 3) |
| FR-04 | A student can leave the queue before being called. | Should | **Yes** | Built (Week 3) |
| FR-05 | A cashier can see the waiting tickets in order. | Must | **Yes** | Built (Week 3) |
| FR-06 | A cashier can call the next ticket with one click, and the called number is shown in big numbers. | Must | **Yes** | Built (Week 3) |
| FR-07 | A cashier can mark a called ticket as served. | Must | **Yes** | Built (Week 3) |
| FR-08 | A cashier can mark a called ticket as no-show. | Must | **Yes** | Built (Week 3) |
| FR-09 ★ | A cashier can see how many students are waiting for each service and filter the list by service. | Could | No | Built (Week 3) |
| FR-10 | A cashier can log in so that only staff can change tickets. | Should | **Yes** | Later |
| FR-11 ★ | A student can choose one of three cashier services when joining: Registrar document fees, Tuition and other fees, or Other payments. | Must | **Yes** | Built (Week 3) |
| FR-12 ★ | A cashier can add, rename and switch off a service. | Must | **Yes** | This week |


### Non-functional requirements

| ID | Requirement | Category | Priority |
| --- | --- | --- | --- |
| NFR-01 | A student’s ticket status and position update within 10 seconds of a cashier action, without the need to reload the page. Each page loads in less than 3 seconds on a mobile connection. | Performance | Must |
| NFR-02 | A first-time student can get in line and get their ticket number in less than 2 minutes without assistance when they use the app. Additionally, the pages are going to be375 px wide, without side scrolling and the main buttons are at least 44 px tall. | Usability | Must |
| NFR-03 | A first-time student can get in line and get their ticket number in less than 2 minutes without assistance. Pages are 375 px wide, with no side scrolling. The main buttons are at least 44 px tall. | Security / privacy | Must |
| NFR-04 | The app works on any of the latest versions of Chrome on all devices like phones and laptops, and doesn't need to be downloaded from any app stores. | Compatibility | Should |
| NFR-05 | No tickets are lost or erased when Flask or the database restarts. After `docker compose down` and `up`  commands, each ticket has to retain the same status and time as before. | Reliability | Must |

## MVP

**MVP:** FR-01, FR-02, FR-05, FR-06, FR-07, FR-08, FR-11, FR-12, plus NFR-01, NFR-02, NFR-03 and NFR-05.

This is the smallest version that still solves the problem: a student can join from their phone, see their place and be called. For the cashier's side, they can run the whole line from one dashboard, the tickets are stored in a database and are still there after the server is restarted. Features like leaving the queue or filtering by service are useful, but the app still works without them, so they can wait until later.

## Out of scope

- **SMS or email alerts:** Students see updates only by keeping the page open, since sending messages needs extra setup and cost.
- **Native mobile app:** The web app already works on any phone, and a separate app takes more time and skills.
- **Paying inside the app:** The app only manages the line, so students still pay at the cashier window.

## Feedback from a person in my setting

| Who (role only, no full name)| What they said | What I changed |
| --- | --- | --- |
| 3rd-year student| They made a suggestion about adding an alert that will notify their position in the queue, e.g two students are ahead of them so the system should notify them that. This way, the students can do other things while waiting and not miss their turn. They also said that every funtional requirements I presented are all equally important. Lastly, they listed FR-01, FR-05 and FR-07 as the 3 functional requirements when answering the 3rd question | I didn't add new functional requirements based on what they had answered. As for their suggestion, the current ticket page already shows the student's place and a "You're next!" message (FR-02, FR-03). However, adding alerts that would send timely notifications on devices (such as SMS, email, phone notifications) are out of scope. |