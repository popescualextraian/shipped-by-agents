# Migrating Legacy Java to Modern Stacks with AI Coding Agents

*How AI coding agents turn a two-year migration into a three-month sprint*

---

You know the system. Every company has one. The booking platform built in 2009. The HR portal from 2012. The inventory system that "just works" — until it doesn't, and nobody remembers why.

It runs on EJB 2.1, deployed on WebSphere. The frontend is Dojo Toolkit — a framework so old that Stack Overflow questions about it have cobwebs. The original developers left years ago. The documentation, if it ever existed, is a lie.

You've wanted to migrate for years. But the estimate always comes back the same: 18–24 months, a dedicated team of six, and a budget that makes leadership wince. So the system stays. Another year. Another patch. Another developer who quits rather than maintain it.

**That calculation just changed.**

AI coding agents — GitHub Copilot, Claude Code, Amazon Q, Cursor — have fundamentally altered what a small team can accomplish. Not by writing perfect code (they don't), but by doing the tedious, repetitive, analytical work that makes migrations take years instead of months.

The numbers are real:

| Metric | Source |
|--------|--------|
| Amazon migrated thousands of Java apps, saving 4,500 developer-years | AWS |
| Cognizant achieved 93% accuracy on COBOL-to-Java transformation | Anthropic |
| Teams report 40–60% reduction in migration timelines | Multiple sources |
| AI-assisted component refactoring automates 60–80% of structural work | LegacyLeap |
| A Struts2-to-Spring Boot migration completed in 1 hour with Claude Code | DEV Community |

This article is a practical guide to making that happen. It follows TravelCorp — a fictional but realistic company — through a full migration from EJB + Dojo to Spring Boot + React. The strategies are generic. The examples are specific. The goal is speed.

---

## 1. Set Up Your AI Workspace

Before you ask the AI a single question about your legacy code, prepare the ground. The quality of your migration depends on the quality of context you give your tools.

### 1.1 Create project instruction files

Every AI coding tool supports some form of persistent project context. Use it.

**For Claude Code — `CLAUDE.md`:**

```markdown
# Legacy Booking Platform — Migration Project

## System Overview
Internal travel booking platform. In production since 2009.
- Backend: EJB 2.1 on IBM WebSphere 8.5
- Frontend: Dojo Toolkit 1.9 with Dijit widgets
- Database: Oracle 12c, ~180 tables
- Build: Ant + IBM RAD
- Lines of code: ~200K Java, ~80K JavaScript

## Architecture
- 47 stateless session beans (business logic)
- 12 stateful session beans (wizard flows, shopping cart)
- 8 message-driven beans (async processing: email, PDF generation, payment callbacks)
- 230 Dojo widgets (mix of Dijit and custom)
- JNDI for all resource lookups
- Container-managed transactions (CMT) everywhere

## Migration Target
- Spring Boot 3.x with embedded Tomcat
- React 18 with TypeScript
- PostgreSQL (from Oracle)
- REST API layer between frontend and backend

## Constraints
- Three-person team
- Must maintain production availability during migration
- No big-bang cutover — incremental only
- Payment module is PCI-compliant — extra review required

## Conventions
- Java: follow existing package structure (com.travelcorp.*)
- React: functional components with hooks, no class components
- Tests: JUnit 5 for backend, React Testing Library for frontend
- All AI-generated code must be reviewed before merge
```

**For GitHub Copilot — `.github/copilot-instructions.md`:**

Same content, different file. Copilot reads this automatically in VS Code and JetBrains IDEs.

**For Cursor — `.cursorrules`:**

Same concept, adapted to Cursor's format.

The point isn't the file format. The point is: **tell the AI what it's looking at before you ask it to work.** Without this, you'll waste hours correcting misunderstandings that a five-minute setup would have prevented.

### 1.2 Feed external context

Your legacy system's truth doesn't live only in code. Gather and make accessible:

- **Architecture diagrams** — even hand-drawn ones scanned to PNG. Claude and Copilot can read images.
- **Deployment documentation** — WebSphere config, JNDI bindings, datasource definitions
- **Database schema** — export DDL scripts, ER diagrams
- **Wiki pages** — if your team has a Confluence or SharePoint with system documentation, export the relevant pages
- **API specs** — if any exist. For legacy systems, they usually don't — you'll generate them.
- **Build scripts** — Ant build.xml, Maven pom.xml, or whatever drives your build. These reveal dependencies the code doesn't show.

### 1.3 Set up memory and skills

If you're using Claude Code, configure memory files for decisions that should persist across sessions:

```markdown
# Migration Decisions (memory)
- Using Strangler Fig pattern — incremental replacement, not big bang
- API-first: REST endpoints are the contract between old and new
- Payment module migrates LAST (PCI compliance review required)
- Stateful beans: externalize state to Redis, not database sessions
```

For Copilot, pin relevant files in your IDE context and use workspace-level instructions. For Cursor, use the Composer's context features to keep architectural decisions visible.

The goal: **any AI session, at any point in the migration, should understand what you're doing and why.**

---

## 2. Understand What You Have

Now use AI as your archaeological tool. The legacy codebase is a dig site — full of buried assumptions, forgotten decisions, and load-bearing hacks.

### 2.1 Automated codebase analysis

Start with broad discovery. Feed your codebase to the AI and ask it to map what exists.

**Prompt — dependency mapping:**
```
Analyze the EJB modules in src/main/java/com/travelcorp/ejb/.
For each session bean, list:
- Bean type (stateless, stateful, MDB)
- JNDI name
- Remote and local interfaces
- Injected dependencies (@EJB, @Resource)
- Transaction attributes (per method if annotated)
- Database tables accessed (via JPA entities or JDBC calls)
```

**Prompt — frontend inventory:**
```
Analyze the Dojo widgets in webapp/js/widgets/. For each widget, list:
- Widget name and AMD module path
- Parent widget (if it extends another)
- Dojo stores or models it binds to
- DOM events it handles
- Server endpoints it calls (look for xhr, request, or fetch calls)
- Dijit components it uses (dijit/form/*, dijit/layout/*, dgrid/*)
```

**Prompt — dead code identification:**
```
Cross-reference the EJB session beans with all JSP pages, Dojo widgets,
and other beans that reference them. Identify beans that have no callers —
they may be dead code we can skip migrating entirely.
```

### 2.2 Business logic extraction

This is where AI pays for itself. Legacy code is full of business rules buried in if-statements, switch blocks, and validation methods. No one remembers them. The documentation is wrong. The code is the only truth.

**Prompt — requirements mining:**
```
Read the BookingService session bean and extract every business rule
it enforces. Express each rule in plain English. For example:
- "A booking cannot be created within 24 hours of departure"
- "Corporate customers receive a 15% discount on domestic flights"
- "Group bookings (5+ passengers) require manager approval"

Include the line numbers where each rule is implemented.
```

This output becomes your **acceptance criteria** for the migrated version. You're not writing requirements from memory or interviewing stakeholders who forgot — you're extracting them directly from the running system.

> **Speed principle:** Extract requirements from code, not from humans. The code remembers what people forgot. AI reads it in minutes. Interviewing stakeholders takes weeks and produces less accurate results.

### 2.3 What TravelCorp discovered

After two days of AI-assisted analysis, TravelCorp's team had:

- A complete inventory: 47 stateless beans, 12 stateful beans, 8 MDBs, 230 Dojo widgets
- 340 business rules extracted and documented — more than anyone on the team knew existed
- 23 EJB beans with zero callers — dead code, never to be migrated
- 41 Dojo widgets used on only one page, 12 of which served pages with zero traffic in the last 90 days
- A dependency graph showing which modules were tightly coupled and which could be extracted independently

That last point matters most. The dependency graph tells you **where to cut** — which modules have clean boundaries and can be migrated first, and which are tangled messes you save for later.

---

## 3. Design the Target Architecture

### 3.1 Generic principles — applicable to any legacy migration

Before choosing specific technologies, apply these universal rules:

**Choose based on your team, not on benchmarks.** The best target stack is the one your team can actually build and maintain. If your developers know Spring, go Spring Boot. If they know Node, go Express or NestJS. A technically superior choice that nobody on the team understands is a technically inferior choice.

**Define the contract first.** The single most important artifact in any migration is the **API contract** between old and new. Whether it's REST, GraphQL, or gRPC — define it before writing a line of code. This contract lets frontend and backend migrate independently, at different speeds, by different people.

**Don't over-decompose.** The urge to go from monolith to microservices during a migration is strong and almost always wrong. Migrate to a **modular monolith** first. You can extract microservices later when you actually understand your domain boundaries. Premature decomposition is how migrations take two years.

**Map old concepts to new ones explicitly.** Create a mapping table for your specific migration:

| Legacy Concept | Modern Equivalent | Notes |
|---|---|---|
| Server-side rendering (JSP, JSF, Dojo server-side) | Single-page application (React, Angular, Vue) | Requires API layer |
| Container-managed services (EJB, managed beans) | Framework dependency injection (@Service, @Component) | Usually 1:1 |
| XML configuration (ejb-jar.xml, web.xml, faces-config.xml) | Annotations + convention over configuration | AI handles this well |
| App server deployment (EAR/WAR on WebSphere/JBoss) | Embedded container (Spring Boot JAR, Docker) | Fundamental packaging change |
| Server-side session state | Stateless + externalized state (JWT, Redis) | Hardest conceptual shift |
| Container-managed transactions | Declarative transactions (@Transactional) | Watch for distributed tx |
| JNDI resource lookups | Dependency injection + config properties | Straightforward |

**Decide what NOT to migrate.** This is your biggest speed lever. After the assessment phase, you have a list of dead code, unused features, and low-traffic pages. **Don't migrate them.** Every feature you skip is weeks saved. Be ruthless.

### 3.2 Migration strategy: Strangler Fig + API-first

The Strangler Fig pattern is the dominant strategy for incremental migration, and for good reason: it's the only approach that lets you ship value continuously while migrating.

The idea is simple:

1. Build a thin API layer in front of the legacy system
2. Route all traffic through it
3. Implement new features (or re-implement old ones) behind the API using the modern stack
4. Gradually shift routing from old to new
5. When nothing routes to the old system, turn it off

Combined with an API-first approach:

```
[Users]
   |
[API Gateway / Reverse Proxy]
   |
   ├── /api/bookings/*  →  [New Spring Boot service]
   ├── /api/users/*     →  [New Spring Boot service]
   ├── /app/bookings/*  →  [New React SPA]
   └── everything else  →  [Legacy WebSphere + Dojo]
```

The API contract is the migration boundary. Old and new coexist. No big-bang cutover. You can stop at any point and the system still works.

### 3.3 Decision framework: migrate, rewrite, wrap, or kill

Not every module gets the same treatment. For each legacy component, choose one:

| Strategy | When to use | Speed | Risk |
|---|---|---|---|
| **Kill** | Dead code, unused features, zero-traffic pages | Instant | None — just verify it's truly unused |
| **Wrap** | Working code that doesn't need to change, just needs a modern API | Fast | Low — you're adding an adapter, not rewriting |
| **Migrate** | Code that needs to move to the new stack but logic stays the same | Medium | Medium — AI handles most of it |
| **Rewrite** | Code that's fundamentally broken or impossible to migrate (rare) | Slow | High — only do this when you must |

Applied to TravelCorp:

- **Kill:** 23 dead EJB beans, 12 zero-traffic Dojo pages → skip entirely
- **Wrap:** Payment processing module → keep on WebSphere behind a REST adapter (PCI compliance, migrate later)
- **Migrate:** 24 stateless beans + 180 Dojo widgets → AI-assisted conversion to Spring Boot + React
- **Rewrite:** The booking wizard (3 stateful beans with deeply coupled Dojo UI) → redesign from scratch using extracted business rules

### 3.4 The "screenshot and spec" strategy: reimplementation over translation

There's a fifth option beyond kill, wrap, migrate, and rewrite — and for some modules it's the fastest of all: **treat the legacy system as a specification and build fresh.**

Instead of reading old Dojo widgets and converting them to React, or tracing EJB call chains and translating them to Spring — you extract the *what* and throw away the *how*.

**Step 1: Capture the legacy system's outputs, not its code.**

| Artifact | How to extract | What it becomes |
|---|---|---|
| **Screenshots** of every page and state | Playwright/Selenium automated crawl, or manual walkthrough | Visual spec for the new UI — feed directly to AI: "Build a React component that looks like this screenshot" |
| **Business rules** in plain English | AI reads the legacy code and writes human-readable requirements (see Section 2.2) | Acceptance criteria and test cases for the new implementation |
| **API request/response pairs** | Record real traffic with a proxy (mitmproxy, Fiddler), or instrument the legacy app | Contract spec — the new backend must produce identical responses |
| **Data models** | Export DDL, generate ER diagrams, dump sample data | Schema for the new system — often reusable as-is |
| **User flows** | Screen recordings or step-by-step documented workflows | UX spec for the new frontend |
| **Error messages and edge cases** | Crawl logs, support tickets, error handling code | Negative test cases the new system must handle |

**Step 2: Feed these artifacts as prompts for a fresh build.**

```
Prompt (with screenshot attached):
Here is a screenshot of our legacy booking search results page.
Build a React component using TypeScript and MUI that:
- Reproduces this layout and visual hierarchy
- Fetches data from GET /api/flights?origin={}&dest={}&date={}
- Supports sorting by price, duration, and departure time
- Handles the loading and error states shown in screenshots 2 and 3

Here are the business rules this page must enforce:
1. Display max 50 results
2. Sold-out flights appear grayed out but visible
3. Corporate users see a "negotiated rate" badge on eligible flights
```

**Why this is sometimes faster than code translation:**

- **No framework baggage.** You skip understanding Dojo's AMD modules, widget lifecycle, and store system entirely. The AI generates idiomatic React from a visual spec — clean, modern code that doesn't carry legacy patterns.
- **Better architecture.** Translated code inherits the old system's design decisions. Reimplemented code gets a fresh architecture. A Dojo widget with 400 lines of imperative DOM manipulation becomes a 60-line React component.
- **Multimodal AI excels here.** Claude and GPT-4o can look at a screenshot and generate surprisingly accurate UI code. This capability didn't exist two years ago. Use it.
- **Parallel workstreams.** Frontend reimplementation from screenshots can start immediately — it doesn't depend on the backend migration. The API contract (captured from real traffic) is the only dependency.

**When to use this strategy:**

- Complex UI components where the visual behavior matters more than the code structure
- Pages with heavy legacy framework coupling (deep Dijit inheritance chains, custom Dojo mixins)
- Modules where the legacy code is so convoluted that understanding it takes longer than rebuilding
- When you have good screenshot/recording coverage of the existing system

**When NOT to use it:**

- Backend business logic with subtle rules and edge cases — here you need code-level extraction, not screenshots
- Components with complex state management that isn't visible in the UI
- Anything involving security, authentication, or payment — too risky to reimplement from visual spec alone

**TravelCorp used this for the seat map.** The legacy seat map was a 2,000-line Dojo widget with SVG rendering, custom event handling, and three levels of class inheritance. Instead of translating it, they:
1. Captured screenshots of every seat state (available, selected, occupied, premium, exit row)
2. Recorded the API contract (GET /api/flights/{id}/seatmap → JSON seat grid)
3. Fed both to Claude: "Build a React seat map component from these screenshots and this API"
4. Got a working 300-line React component in 2 hours. Manual testing and refinement took another 4 hours. Total: 6 hours vs. an estimated 3 days for code translation.

### 3.5 TravelCorp's specific architecture

With the generic principles applied:

**Backend:** EJB 2.1 → Spring Boot 3.x
| EJB Concept | Spring Equivalent |
|---|---|
| `@Stateless` session bean | `@Service` + `@Component` |
| `@Stateful` session bean | Stateless service + Redis for session state |
| `@MessageDriven` bean | `@JmsListener` / Spring Kafka listener |
| Container-managed transactions (CMT) | `@Transactional` |
| `@EJB` / `@Resource` injection | `@Autowired` / constructor injection |
| JNDI lookups | `application.yml` + `@Value` / `@ConfigurationProperties` |
| Entity beans (CMP/BMP) | Spring Data JPA + Hibernate |
| JAAS security | Spring Security + OAuth2/JWT |
| EAR/WAR on WebSphere | Executable JAR with embedded Tomcat |
| `ejb-jar.xml` / `web.xml` | Annotations + `application.yml` |

**Frontend:** Dojo 1.9 → React 18 + TypeScript
| Dojo Concept | React Equivalent |
|---|---|
| Dijit widget | React functional component |
| `declare()` class inheritance | Composition + hooks |
| AMD `define()` / `require()` | ES module `import` / `export` |
| Dojo `topic.publish()` / `subscribe()` | React Context, Redux, or Zustand |
| `dojo/store` / `dstore` | TanStack Query (server state) + Zustand (client state) |
| dgrid | AG Grid or TanStack Table |
| Dijit form widgets | React Hook Form + component library (MUI, Ant Design) |
| Dojo `on()` event handling | React synthetic events (`onClick`, `onChange`) |
| `buildRendering()` / `postCreate()` lifecycle | `useEffect` / `useRef` hooks |
| Dojo build system | Vite or Webpack |

---

## 4. Map Before You Move: Function Parity Analysis

Before writing a single line of new code, answer this question: **what does the old system actually do, and how much of it do you need?**

### 4.1 Build the parity matrix

Use AI to generate a complete inventory of the legacy system's capabilities, then map each one to its modern equivalent.

**Prompt:**
```
For each public method in the BookingService, FlightSearchService, and
UserManagementService EJB beans, create a table with:
- Method name and signature
- Business purpose (one sentence)
- Input/output types
- Called by (which JSPs, widgets, or other beans invoke it)
- Call frequency (if logs are available)
- Mapping type: 1:1, merge, split, deprecate, or new
```

### 4.2 Understand the mapping types

Not everything is a 1:1 conversion. Recognizing this early saves you from migrating things that shouldn't exist in the new system.

**1:1 mappings — the bulk of your work.** The old function maps directly to a new one. Same inputs, same outputs, same business logic. AI handles these almost autonomously. Batch-convert them.

```
Old: BookingService.createBooking(BookingRequest) → BookingResponse
New: BookingController.createBooking(BookingRequest) → BookingResponse
```

**Many-to-one — simplification opportunities.** Multiple legacy functions that exist because of historical accidents. In the new system, they collapse into one.

```
Old: ReportService.getDailyReport(), ReportService.getWeeklyReport(),
     ReportService.getMonthlyReport()  — identical logic, different date ranges
New: ReportController.getReport(dateRange) — one endpoint, parameterized
```

**One-to-many — decomposition required.** A monolithic legacy function doing too many things. Split it into focused services.

```
Old: BookingService.processBooking() — validates, prices, reserves,
     charges, emails, generates PDF, updates loyalty points (800 lines)
New: ValidationService.validate(), PricingService.calculate(),
     ReservationService.reserve(), PaymentService.charge(),
     NotificationService.notify() — each under 100 lines
```

**Deprecate — your biggest speed win.** Legacy functions nobody uses. AI helps identify them through call graph analysis and (if available) log analysis. Every function you don't migrate is time you save.

```
Old: BookingService.createTelex() — sends booking confirmations via Telex.
     Last called: 2014. Kill it.
```

**New — defer it.** Capabilities the modern stack enables that didn't exist before. Resist the urge. Migrate first, enhance later. Mixing migration with feature development is how projects miss deadlines.

### 4.3 The speed math

TravelCorp's parity analysis revealed:

| Mapping Type | Count | % of Total | Migration Effort |
|---|---|---|---|
| 1:1 (direct conversion) | 186 functions | 60% | AI-assisted, fast |
| Many-to-one (merge) | 47 functions → 18 | 15% | Moderate — needs design decisions |
| One-to-many (split) | 31 functions → 74 | 10% | Needs careful decomposition |
| Deprecate (kill) | 46 functions | 15% | Zero — just don't migrate them |

That last row is the headline: **15% of the system doesn't need to be migrated at all.** In a two-year project, that's three months saved — before you write a line of code.

The parity matrix becomes your migration backlog. Prioritize by business value, not technical complexity. Migrate the booking flow first (high value, high traffic), not the admin reporting module (low traffic, used by three people).

---

## 5. Migrate the Backend

### 5.1 Generic strategies — applicable to any backend migration

#### Strategy: Test first, migrate second

The safest and fastest migration strategy is counterintuitive: **write tests before you migrate.**

Not unit tests for the legacy code — that ship sailed years ago. **Characterization tests**: tests that capture the current behavior of the system, whether that behavior is correct or not.

```
Prompt:
Read the BookingService.createBooking() method and generate JUnit 5
characterization tests that cover:
- Every code path (happy path + all error conditions)
- Every business rule enforced
- Edge cases visible in the code (null handling, boundary values)
- The exact exceptions thrown for each failure mode

These tests must pass against the CURRENT implementation. They document
what the system does today, not what it should do.
```

Why this is faster:
- You have a safety net before you touch anything
- The tests become your migration acceptance criteria
- AI generates characterization tests in hours, not weeks
- When the migrated code passes the same tests, you know it works

#### Strategy: Extract the API layer first

Before migrating any business logic, create the REST API that the new frontend will consume. This API initially delegates to the legacy backend.

```java
// Step 1: Thin API wrapper over legacy EJB (runs on a new Spring Boot app)
@RestController
@RequestMapping("/api/bookings")
public class BookingController {

    // Calls the legacy EJB via remote interface or direct JNDI lookup
    @Autowired
    private LegacyBookingBridge legacyBridge;

    @PostMapping
    public BookingResponse createBooking(@RequestBody BookingRequest request) {
        // For now, just delegate to the old system
        return legacyBridge.createBooking(request);
    }
}
```

```java
// Step 2: Later, swap the bridge for the real Spring service
@RestController
@RequestMapping("/api/bookings")
public class BookingController {

    @Autowired
    private BookingService bookingService; // New Spring service

    @PostMapping
    public BookingResponse createBooking(@RequestBody BookingRequest request) {
        return bookingService.createBooking(request);
    }
}
```

The frontend never knows the difference. The API contract stays the same. You can swap implementations behind it at any pace.

#### Strategy: Bulk-convert the easy wins

Stateless, side-effect-free components are migration gold. They're predictable, testable, and AI converts them with high accuracy. Do them first, do them in bulk.

**Prompt for batch conversion:**
```
Convert the following stateless EJB session beans to Spring @Service classes:
- FlightSearchService
- PricingService
- SeatMapService
- AirportLookupService

For each:
1. Remove all EJB annotations (@Stateless, @Local, @Remote)
2. Add @Service annotation
3. Replace @EJB injections with @Autowired (or constructor injection)
4. Replace @Resource JNDI lookups with @Value or @ConfigurationProperties
5. Replace @TransactionAttribute with @Transactional where needed
6. Keep all business logic unchanged
7. Generate a JUnit 5 test class that covers all public methods
```

#### Strategy: Isolate the hard parts

Stateful beans, distributed transactions, and deeply coupled modules are where AI struggles and humans earn their pay. Isolate these, migrate them last, and give them disproportionate attention.

Common hard patterns:
- **Stateful session beans** — conversational state must be externalized (Redis, database). AI generates plausible but often incorrect state management. Review carefully.
- **Distributed transactions** — EJB's container-managed JTA transactions spanning multiple resources don't have a simple Spring equivalent. Consider the Saga pattern or Atomikos for JTA.
- **App server–specific features** — WebSphere work managers, JBoss-specific classloading, WebLogic clustering. These require manual research.

### 5.2 EJB to Spring Boot — specific techniques

Here's what the conversion looks like in practice, pattern by pattern.

#### Stateless session beans → Spring services

The most common conversion. AI handles this with ~95% accuracy.

**Before (EJB):**
```java
@Stateless
@Local(FlightSearchLocal.class)
@Remote(FlightSearchRemote.class)
@TransactionAttribute(TransactionAttributeType.REQUIRED)
public class FlightSearchBean implements FlightSearchLocal, FlightSearchRemote {

    @PersistenceContext(unitName = "travelPU")
    private EntityManager em;

    @EJB
    private PricingLocal pricingService;

    @Resource(mappedName = "java:comp/env/maxResults")
    private int maxResults;

    public List<Flight> search(SearchCriteria criteria) {
        TypedQuery<Flight> query = em.createQuery(
            "SELECT f FROM Flight f WHERE f.origin = :origin AND f.destination = :dest " +
            "AND f.departureDate = :date", Flight.class);
        query.setParameter("origin", criteria.getOrigin());
        query.setParameter("dest", criteria.getDestination());
        query.setParameter("date", criteria.getDate());
        query.setMaxResults(maxResults);

        List<Flight> flights = query.getResultList();
        flights.forEach(f -> f.setPrice(pricingService.calculate(f)));
        return flights;
    }
}
```

**After (Spring Boot):**
```java
@Service
@Transactional(readOnly = true)
public class FlightSearchService {

    private final FlightRepository flightRepository;
    private final PricingService pricingService;

    @Value("${search.max-results:50}")
    private int maxResults;

    public FlightSearchService(FlightRepository flightRepository,
                                PricingService pricingService) {
        this.flightRepository = flightRepository;
        this.pricingService = pricingService;
    }

    public List<Flight> search(SearchCriteria criteria) {
        List<Flight> flights = flightRepository
            .findByOriginAndDestinationAndDepartureDate(
                criteria.getOrigin(),
                criteria.getDestination(),
                criteria.getDate(),
                PageRequest.of(0, maxResults));

        flights.forEach(f -> f.setPrice(pricingService.calculate(f)));
        return flights;
    }
}
```

What changed:
- `@Stateless` → `@Service`
- `@EJB` → constructor injection
- `@Resource` JNDI lookup → `@Value` with default
- `@TransactionAttribute` → `@Transactional`
- Manual JPQL → Spring Data JPA repository method
- Remote/local interfaces → gone (REST API replaces remote access)

#### Stateful session beans → stateless services + externalized state

This is the hardest pattern. EJB stateful beans maintain conversational state between calls — the booking wizard that remembers your selections across pages. Spring Boot is stateless by design.

**Before (EJB):**
```java
@Stateful
@SessionScoped
public class BookingWizardBean {

    private FlightSelection selectedFlight;
    private List<Passenger> passengers;
    private PaymentInfo payment;
    private BookingState state = BookingState.FLIGHT_SEARCH;

    public void selectFlight(FlightSelection flight) {
        this.selectedFlight = flight;
        this.state = BookingState.PASSENGER_DETAILS;
    }

    public void addPassengers(List<Passenger> passengers) {
        this.passengers = passengers;
        this.state = BookingState.PAYMENT;
    }

    public BookingConfirmation confirm() {
        // Uses all accumulated state to create booking
        return createBooking(selectedFlight, passengers, payment);
    }

    @Remove
    public void cancel() {
        // EJB container removes the bean
    }
}
```

**After (Spring Boot + Redis):**
```java
@Service
public class BookingWizardService {

    private final RedisTemplate<String, WizardSession> redisTemplate;
    private final BookingService bookingService;

    public WizardSession selectFlight(String sessionId, FlightSelection flight) {
        WizardSession session = getOrCreateSession(sessionId);
        session.setSelectedFlight(flight);
        session.setState(BookingState.PASSENGER_DETAILS);
        redisTemplate.opsForValue().set(sessionId, session, 30, TimeUnit.MINUTES);
        return session;
    }

    public WizardSession addPassengers(String sessionId, List<Passenger> passengers) {
        WizardSession session = getSession(sessionId);
        session.setPassengers(passengers);
        session.setState(BookingState.PAYMENT);
        redisTemplate.opsForValue().set(sessionId, session, 30, TimeUnit.MINUTES);
        return session;
    }

    public BookingConfirmation confirm(String sessionId) {
        WizardSession session = getSession(sessionId);
        BookingConfirmation confirmation = bookingService.createBooking(
            session.getSelectedFlight(),
            session.getPassengers(),
            session.getPayment());
        redisTemplate.delete(sessionId);
        return confirmation;
    }
}
```

The conversational state moves from the EJB container's memory to Redis. The service itself becomes stateless — any instance can handle any request. This is where AI often gets it wrong: it generates code that looks right but doesn't handle session expiration, concurrent access, or serialization edge cases. **Review stateful bean conversions manually.**

#### Message-driven beans → Spring JMS listeners

Straightforward conversion. AI handles this well.

**Before (EJB):**
```java
@MessageDriven(activationConfig = {
    @ActivationConfigProperty(propertyName = "destinationType",
                              propertyValue = "javax.jms.Queue"),
    @ActivationConfigProperty(propertyName = "destination",
                              propertyValue = "queue/EmailQueue")
})
public class EmailNotificationMDB implements MessageListener {

    @EJB
    private EmailService emailService;

    @Override
    public void onMessage(Message message) {
        TextMessage textMessage = (TextMessage) message;
        EmailRequest request = deserialize(textMessage.getText());
        emailService.send(request);
    }
}
```

**After (Spring Boot):**
```java
@Component
public class EmailNotificationListener {

    private final EmailService emailService;

    public EmailNotificationListener(EmailService emailService) {
        this.emailService = emailService;
    }

    @JmsListener(destination = "email-queue")
    public void onMessage(EmailRequest request) {
        emailService.send(request);
    }
}
```

Simpler, cleaner, and Spring handles the deserialization. The `@JmsListener` annotation replaces the entire MDB lifecycle.

#### App server extraction: WebSphere/JBoss → embedded Tomcat

This isn't a code change — it's a paradigm shift. Traditional app servers treat infrastructure as the runtime. Spring Boot treats the application as the runtime.

Key changes:
- **EAR/WAR packaging** → executable JAR (`mvn spring-boot:repackage`)
- **Deployment descriptors** (`ejb-jar.xml`, `web.xml`, `application.xml`) → `application.yml` + annotations
- **JNDI datasources** → `spring.datasource.*` properties
- **App server JMS** → embedded ActiveMQ/Artemis or external broker config
- **Classloader hierarchy** → flat classpath (this solves more problems than you'd expect)

**Prompt for app server extraction:**
```
Analyze the following WebSphere-specific configuration files and generate
the equivalent Spring Boot application.yml:
- server.xml (datasources, JMS queues, connection pools)
- ejb-jar.xml (transaction attributes, security roles)
- web.xml (servlet mappings, filters, security constraints)
- ibm-web-bnd.xml (WebSphere bindings)
```

### 5.3 Tooling for backend migration

Don't rely on AI alone. Combine it with purpose-built migration tools:

| Tool | Best for | How it helps |
|---|---|---|
| **Spring Boot Migrator (SBM)** | EJB → Spring Boot | OpenRewrite recipes for stateless EJB, deployment descriptors, WebLogic/WebSphere configs |
| **OpenRewrite** | Automated code transformations | Chainable recipes: Java 8→17 + javax→jakarta + Spring Boot 2→3 in one pass |
| **GitHub Copilot App Modernization** | Java version upgrades | Agent-mode: analyze → plan → transform → fix → validate → scan CVEs |
| **Amazon Q Developer Transform** | Java EE → Spring Boot at scale | Converts servlets to @RestController, refactors JDBC to JPA, handles SDK migration |
| **Claude Code** | Complex refactoring, large context analysis | Best for understanding tangled legacy code, extracting business rules, multi-file refactoring |

The most effective workflow: use **SBM/OpenRewrite** for mechanical transformations (annotations, imports, config), then **Claude or Copilot** for the parts that require understanding (business logic, state management, edge cases).

### 5.4 TravelCorp's backend migration

Timeline: 4 weeks for the backend.

**Week 1:** AI generates characterization tests for all 47 stateless beans (380 test methods). Team reviews and fills gaps. Creates REST API shell with legacy bridge.

**Week 2:** Batch-convert all stateless beans using Claude Code. SBM handles deployment descriptor migration and javax→jakarta namespace change. 40 of 47 beans convert cleanly. 7 need manual fixes (complex JPQL queries, WebSphere-specific API calls).

**Week 3:** Tackle the 8 MDBs (straightforward) and start on the 12 stateful beans (not straightforward). The booking wizard requires a full redesign — business rules extracted in the assessment phase become the spec.

**Week 4:** Finish stateful bean migration. Payment module stays wrapped behind a REST adapter on WebSphere. Integration testing against the characterization tests — 94% pass on first run. The 6% that fail reveal genuine bugs in the conversion that AI missed, mostly around transaction boundary differences.

---

## 6. Migrate the Frontend

### 6.1 Generic strategies — applicable to any frontend migration

Frontend migration is fundamentally different from backend migration. Backend code is logic — functions, data, rules. Frontend code is **experience** — layout, interaction, visual feedback. You can test logic with assertions. You test experience with your eyes.

#### Strategy: Define the component inventory

Before converting anything, catalog what you have. Every legacy framework — Dojo, ExtJS, jQuery UI, YUI, GWT — has its own component model. Map it.

**Prompt:**
```
Analyze all Dojo widgets in webapp/js/widgets/. Create a table:
- Widget name
- Type (form input, layout container, data display, navigation, dialog)
- Complexity (simple: <100 lines, medium: 100-300, complex: 300+)
- Dependencies (other widgets, stores, server calls)
- Page(s) where it's used
- Usage frequency (if analytics data available)
```

#### Strategy: Pick your interop bridge

You will not convert everything at once. You need old and new to coexist. Choose your bridge technology:

| Approach | How it works | Best when |
|---|---|---|
| **New components inside old shell** | React components rendered into DOM nodes that the legacy framework manages | Legacy framework controls routing and page layout |
| **Old components inside new shell** | Legacy widgets wrapped as React components | React controls routing, legacy components are being phased out |
| **Micro frontends** | Independent apps (old and new) composed at the page or route level | Separate teams or very large applications |
| **Page-by-page replacement** | Entire pages rebuilt in React, routing splits traffic | Clean page boundaries, minimal cross-page state |

For most migrations, **page-by-page replacement** combined with **new-inside-old** for shared components is the fastest path.

#### Strategy: Don't replicate — simplify

Legacy frontends accumulate cruft. Custom dropdown components written because the browser native one didn't support a feature in IE8. Layout hacks for quirks mode. Animation code for long-forgotten marketing requirements.

When you migrate, you're not copying the old UI pixel-for-pixel. You're building the UI **that should have existed** given today's browsers and design systems.

This means:
- Replace 15 custom form components with a component library (MUI, Ant Design, shadcn/ui)
- Replace custom grid implementations with AG Grid or TanStack Table
- Replace layout hacks with CSS Grid / Flexbox
- Replace custom state management with React state patterns

**This is another speed lever: don't rebuild complexity that modern tools make unnecessary.**

### 6.2 Dojo to React — specific techniques

Dojo Toolkit is a particular challenge because:
- Its AMD module system (`define`, `require`) is incompatible with modern ES modules
- Its widget lifecycle (`buildRendering`, `postCreate`, `startup`, `destroy`) doesn't map neatly to React
- Its class system (`declare`) uses multiple inheritance, which React's composition model doesn't support
- There are no automated Dojo-to-React conversion tools
- Community resources are scarce — Dojo is niche

This makes AI tools more valuable, not less. The AI doesn't need a thriving community — it needs the source code.

#### AMD modules to ES modules

Dojo's AMD module system is the first thing that has to go. You can't import AMD modules into a modern React build.

**Before (Dojo AMD):**
```javascript
define([
    "dojo/_base/declare",
    "dijit/_WidgetBase",
    "dijit/_TemplatedMixin",
    "dojo/text!./templates/FlightCard.html",
    "dojo/store/Memory",
    "dojo/on"
], function(declare, _WidgetBase, _TemplatedMixin, template, Memory, on) {

    return declare([_WidgetBase, _TemplatedMixin], {
        templateString: template,
        baseClass: "flight-card",

        flight: null,

        postCreate: function() {
            this.inherited(arguments);
            this._renderFlight();
            on(this.selectButton, "click", this._onSelect.bind(this));
        },

        _renderFlight: function() {
            this.airlineNode.textContent = this.flight.airline;
            this.priceNode.textContent = "$" + this.flight.price;
            this.timeNode.textContent = this.flight.departure + " → " + this.flight.arrival;
        },

        _onSelect: function() {
            this.emit("flight-selected", { flight: this.flight });
        },

        destroy: function() {
            this.inherited(arguments);
        }
    });
});
```

**After (React):**
```tsx
interface FlightCardProps {
    flight: Flight;
    onSelect: (flight: Flight) => void;
}

export function FlightCard({ flight, onSelect }: FlightCardProps) {
    return (
        <div className="flight-card">
            <span className="airline">{flight.airline}</span>
            <span className="price">${flight.price}</span>
            <span className="time">
                {flight.departure} → {flight.arrival}
            </span>
            <button onClick={() => onSelect(flight)}>
                Select
            </button>
        </div>
    );
}
```

What changed:
- `declare` with mixins → functional component with props
- HTML template file → inline JSX
- `postCreate` lifecycle → not needed (React renders declaratively)
- Manual DOM updates (`textContent`) → JSX expressions (`{flight.airline}`)
- `dojo/on` event binding → React `onClick` prop
- `emit` custom event → callback prop (`onSelect`)
- `destroy` cleanup → not needed (React handles unmounting)

The React version is half the lines, more readable, and has no framework overhead.

**Prompt for batch conversion:**
```
Convert the following Dojo widgets to React functional components
with TypeScript. For each widget:

1. Replace declare() with a functional component
2. Replace the HTML template with JSX
3. Replace postCreate/startup lifecycle with useEffect where needed
4. Replace dojo/on event binding with React event props
5. Replace dojo/store data binding with props or React state
6. Replace topic.publish/subscribe with callback props
7. Use TypeScript interfaces for props
8. Keep the same CSS class names (we'll migrate CSS separately)

Widgets: FlightCard, PassengerForm, SeatMap, BookingSummary, PaymentForm
```

#### Dojo stores to React state management

Dojo's data layer (dojo/store, dstore) uses a different mental model than React. Dojo stores are mutable object stores with query APIs. React state is immutable snapshots with unidirectional data flow.

| Dojo Pattern | React Equivalent |
|---|---|
| `dojo/store/Memory` (local data) | `useState` or `useReducer` |
| `dojo/store/JsonRest` (server data) | TanStack Query / SWR |
| `dstore/Trackable` (observable store) | Zustand or Redux |
| `topic.publish()` / `topic.subscribe()` | React Context, Zustand, or custom events |
| Store query + filter | TanStack Query with server-side filtering |

For most migrations, **TanStack Query for server state + Zustand for client state** is the simplest combination. Don't reach for Redux unless your state management is genuinely complex.

#### The dgrid problem

If your Dojo app uses dgrid (and most enterprise Dojo apps do), you need a React data grid. This is one of the highest-risk components because enterprise grids are feature-dense: sorting, filtering, grouping, inline editing, virtual scrolling, column resizing, export.

Options:

| Library | License | Strengths | Best for |
|---|---|---|---|
| **AG Grid** | MIT (Community) / Commercial (Enterprise) | Most features, best docs, huge ecosystem | Enterprise apps that need everything |
| **TanStack Table** | MIT | Headless — bring your own UI, maximum flexibility | Teams that want full control over rendering |
| **MUI DataGrid** | MIT (basic) / Commercial (Pro/Premium) | Tight MUI integration | Apps already using Material UI |
| **Ant Design Table** | MIT | Good enough for most needs, built into Ant Design | Apps using Ant Design |

**Prompt for dgrid migration:**
```
Analyze the dgrid configurations in our Dojo code. For each grid, list:
- Columns (field name, label, formatter, editor)
- Features used (sorting, filtering, pagination, selection, inline editing)
- Custom renderers or cell formatters
- Data source (store type and endpoint)

Then generate AG Grid equivalents using AG Grid React with TypeScript.
```

### 6.3 The interop bridge in practice

During migration, Dojo and React must coexist. Here's how.

**React component inside a Dojo page:**

```javascript
// Dojo AMD wrapper that renders a React component
define([
    "react",
    "react-dom/client",
    "app/react/FlightCard"
], function(React, ReactDOMClient, FlightCard) {

    return {
        render: function(containerNode, props) {
            const root = ReactDOMClient.createRoot(containerNode);
            root.render(React.createElement(FlightCard, props));
            return {
                destroy: function() { root.unmount(); }
            };
        }
    };
});
```

This lets you replace individual widgets inside existing Dojo pages without rewriting the whole page. The Centric Software team used exactly this approach: identifying "strategic insertion points" where React delivered maximum value with minimal disruption.

**Build system bridge:**

Use `dojo-webpack-plugin` to let Webpack process Dojo AMD modules alongside React ES modules. This lets both worlds share a single build pipeline during the transition.

```javascript
// webpack.config.js — hybrid Dojo + React build
const DojoWebpackPlugin = require("dojo-webpack-plugin");

module.exports = {
    entry: { app: "./src/index.tsx" },
    plugins: [
        new DojoWebpackPlugin({
            loaderConfig: require("./dojo-loader-config"),
            locales: ["en"]
        })
    ],
    module: {
        rules: [
            { test: /\.tsx?$/, use: "ts-loader" },
            { test: /\.css$/, use: ["style-loader", "css-loader"] }
        ]
    }
};
```

### 6.4 TravelCorp's frontend migration

Timeline: 5 weeks for the frontend (overlapping with backend weeks 2–4).

**Week 1:** Set up React project with TypeScript, Vite, and the Dojo interop bridge. Configure hybrid build. Convert the 5 simplest widgets as a proof of concept.

**Week 2:** Batch-convert 80 simple widgets (form inputs, display cards, navigation elements) using Claude. AI handles these with ~90% accuracy. Remaining 10% need manual CSS fixes and event handling adjustments.

**Week 3:** Tackle the data grids. Replace dgrid with AG Grid across 12 pages. This is slower — each grid has custom formatters, editors, and data pipelines that need careful mapping.

**Week 4:** Convert the complex composite widgets (booking wizard UI, seat map, interactive calendar). These can't be bulk-converted — they require understanding the UX flow, not just the code structure. AI extracts the business rules; humans redesign the interaction.

**Week 5:** Integration testing. Visual regression testing (screenshot comparison between old Dojo UI and new React UI). Fix the mismatches — there will be many, mostly CSS and layout differences that don't affect functionality.

---

## 7. Test and Validate

### 7.1 Testing strategy for migrations

Migration testing is different from feature testing. You're not testing whether the software does what it *should* — you're testing whether the new system does what the old system *did.*

#### Characterization tests (the migration safety net)

Generate these first, before migrating anything. They capture current behavior.

**Prompt:**
```
Generate integration tests for the /api/bookings endpoint that test:
- Successful booking creation with valid data
- Every validation rule (use the business rules we extracted earlier)
- Error responses for invalid inputs
- Edge cases: empty passenger list, past departure date, duplicate booking
- Response format: exact JSON structure including all fields

These tests must pass against both the legacy system and the migrated
system. They are the proof of behavioral equivalence.
```

#### Contract tests

If you followed the API-first strategy, the REST API contract is your source of truth. Test both sides of it.

```java
// Contract test: same request produces same response from old and new
@ParameterizedTest
@MethodSource("testCases")
void behavioralEquivalence(BookingRequest request) {
    BookingResponse legacyResponse = legacyClient.createBooking(request);
    BookingResponse newResponse = newClient.createBooking(request);

    assertThat(newResponse)
        .usingRecursiveComparison()
        .ignoringFields("timestamp", "requestId")
        .isEqualTo(legacyResponse);
}
```

#### Visual regression testing

For the frontend, automated visual comparison catches what unit tests miss.

Tools: Playwright screenshot comparison, Percy, Chromatic, or BackstopJS. Configure them to:
1. Render the old Dojo page
2. Render the new React page with the same data
3. Diff the screenshots
4. Flag visual differences above a threshold

Not every difference is a bug. Some are intentional improvements. But you want to know about every one.

#### Performance benchmarks

The new system must not be slower than the old one. Set baselines before migrating and compare after.

Key metrics:
- API response times (p50, p95, p99)
- Page load time (Time to First Byte, Largest Contentful Paint)
- Database query performance
- Memory usage under load

### 7.2 AI-generated test suites

AI is remarkably good at generating tests when given clear specifications. Use the business rules extracted in Section 2 as your spec.

**Prompt:**
```
Given these business rules for the booking system:
1. Bookings cannot be created within 24 hours of departure
2. Maximum 9 passengers per booking
3. Corporate customers receive 15% discount on domestic flights
4. Group bookings (5+ passengers) require manager approval
5. Cancellation is free up to 48 hours before departure

Generate a comprehensive test suite using JUnit 5 and AssertJ that tests
each rule, its boundary conditions, and combinations of rules.
Also generate React Testing Library tests for the booking form that
validates these same rules on the frontend.
```

### 7.3 TravelCorp's testing results

- AI generated 420 characterization tests in one day
- 94% passed against the migrated backend on first run
- The 6% that failed revealed:
  - 3 genuine bugs in AI-converted code (transaction boundary differences)
  - 2 cases where the legacy system had bugs that the tests faithfully captured (migrated code was actually correct)
  - 1 edge case in date handling (timezone conversion difference between WebSphere and embedded Tomcat)
- Visual regression testing flagged 47 layout differences, of which 38 were intentional improvements and 9 were genuine bugs

---

## 8. The Cutover

### 8.1 Go live without going down

The whole point of Strangler Fig is that cutover is gradual, not sudden. But you still need a plan.

**Phase 1: Shadow mode (1 week)**
Route all traffic to both old and new systems. Only the old system serves responses. Compare results. Fix discrepancies.

**Phase 2: Canary release (1–2 weeks)**
Route 5% of traffic to the new system. Monitor error rates, response times, and user feedback. Increase to 10%, 25%, 50%.

**Phase 3: Majority traffic (1–2 weeks)**
Route 90% to new, 10% to old (as fallback). The old system is now the backup.

**Phase 4: Decommission (when ready)**
Route 100% to new. Keep the old system running but unused for 2–4 weeks as insurance. Then turn it off.

### 8.2 Rollback strategy

The old system is still there. That's your rollback. If anything goes wrong at any phase, flip the routing back. This is why Strangler Fig works: you never burn bridges until the new path is proven.

**Feature flags** for fine-grained control:
```yaml
# feature-flags.yml
booking-flow:
  new-react-ui: true        # Serve React booking flow
  new-spring-backend: true   # Use Spring Boot booking service
  legacy-fallback: true      # If Spring fails, fall back to EJB

payment-module:
  new-spring-backend: false  # Still on WebSphere (PCI migration pending)
```

### 8.3 TravelCorp's rollout

- **Week 1:** Shadow mode. Discovered 2 discrepancies in currency formatting and 1 missing error code.
- **Weeks 2–3:** Canary at 5% → 25% → 50%. No issues beyond minor CSS tweaks.
- **Week 4:** 95% on new system. 5% legacy for the payment module (still on WebSphere).
- **Week 8:** Payment module migrated and validated. Legacy WebSphere shut down.

Total elapsed time: **12 weeks from project start to legacy decommission.** Not 18–24 months.

---

## 9. What Slows You Down

Every migration that takes two years started as a project that was supposed to take six months. Here's what goes wrong.

### The big-bang rewrite trap

"Let's just rewrite it from scratch." This sounds liberating. It's almost always fatal.

Netscape rewrote their browser from scratch in 1998. It took three years. During that time, Internet Explorer released two major versions and Netscape lost the browser war. Joel Spolsky called it "the single worst strategic mistake that any software company can make."

The problem: messy legacy code contains years of accumulated bug fixes, edge-case handling, and business logic that nobody remembers. When you rewrite, you lose all of it. The rewrite looks clean for the first few months. Then the edge cases start appearing. Then the schedule slips. Then it slips again.

**Use Strangler Fig. Migrate incrementally. Ship every week.**

### Trusting AI output blindly

AI-generated code looks correct. It compiles. It often even passes basic tests. But it can be subtly wrong, especially in:

- **Authentication and authorization** — AI may generate code that looks secure but has logic flaws
- **Transaction boundaries** — AI doesn't always understand where transactions should start and end in your specific business context
- **Concurrency** — race conditions, deadlocks, and state corruption are hard for AI to reason about
- **Data migration** — charset encoding, timezone handling, null vs. empty string semantics

**Rule: treat AI output as work from a productive but junior developer. Review everything. Trust nothing blindly.**

### The "90% done" illusion

AI gets you to 90% fast. Terrifyingly fast. The first 80% of the migration might take 3 weeks. The last 20% takes another 6 weeks. This is normal. The last 20% is where:

- Edge cases live
- Undocumented business rules hide
- Performance differences surface
- Integration issues appear

Plan for it. Budget 40% of your time for the "last 20%."

### Migrating what nobody uses

The most expensive feature to migrate is the one nobody needs. AI-assisted dead code analysis and usage analytics should happen **before** you start. TravelCorp skipped 15% of their codebase — that's 6+ weeks of work avoided.

### Feature creep during migration

"While we're at it, let's also add..." No. Migration and feature development are two separate workstreams. Mixing them is how timelines double. Migrate first. Enhance later. The only exception: if a feature is genuinely broken in the legacy system and must be fixed to migrate (rare).

### Undocumented dependencies

One team discovered mid-migration that a critical billing function depended on an FTP server that wasn't in any architecture diagram. It delayed the project by months.

AI can help find these: "Analyze all external connections in the codebase — database connections, HTTP calls, file system access, FTP, SMTP, LDAP, message queues. List every external system this application communicates with."

---

## 10. Tool Guide: Choosing Your AI Coding Agent

Here's the honest take: **GitHub Copilot and Claude are similar in capability.** Both can analyze legacy code, generate conversions, write tests, and handle multi-file refactoring. The idea that one has dramatically better "IDE integration" or that the other is fundamentally more powerful is mostly myth at this point. Both tools are agentic, both handle large contexts, and both work well for migration tasks.

That said, most enterprise teams have Copilot through their GitHub license. Some also have access to Claude. Here's how to think about it.

### The tools are interchangeable for most migration work

Every strategy in this article works with either tool. Bulk bean conversion, characterization test generation, business logic extraction, Dojo widget conversion — Copilot and Claude both handle these well. Don't overthink the tool choice. Pick what your team has access to and start.

Where Claude tends to produce slightly better results:
- Very complex legacy code with deep nesting and implicit business rules
- Multi-file architectural reasoning where you need the AI to hold a lot of context simultaneously
- Generating human-readable specifications from undocumented code

But "slightly better" doesn't mean Copilot can't do it. It can. You may need to break the work into smaller chunks or provide more explicit context.

### Strong recommendation: use the CLI

Whatever tool you choose, **use it from the terminal, not just the IDE.**

**GitHub Copilot CLI** and **Claude Code** (or **OpenCode** as an open-source alternative) are where the real migration power lives. The terminal agent can:
- Read and write multiple files in a single session
- Run build commands and fix errors iteratively
- Execute multi-step migration plans autonomously
- Process entire directories of legacy code in batch

### Use Claude for initial planning, Copilot for execution (if you have both)

If your team has access to both tools, here's a practical division:

1. **Claude for the upfront analysis** — feed it the entire legacy codebase, generate the dependency map, extract business rules, build the parity matrix. Claude's strength in producing structured, comprehensive analysis from large codebases gives it an edge here.

2. **Either tool for the conversion work** — once you have the plan, the actual bean-by-bean, widget-by-widget conversion is mechanical enough that both tools perform well.

3. **Either tool for testing and validation** — both generate good characterization tests and integration tests from specs.

If you only have one tool, use that one for everything. The strategies matter more than the tool.

### Purpose-built migration tools

Don't rely only on general-purpose AI. These specialized tools handle specific migration tasks better:

| Tool | Purpose | When to use |
|---|---|---|
| **GitHub Copilot App Modernization** | Java version upgrades (8→17→21), Spring Boot migration, CVE scanning | When you need to upgrade Java versions as part of the migration |
| **Amazon Q Developer Transform** | Java EE → Spring Boot, servlet → @RestController, JDBC → JPA | When targeting AWS deployment, or for large-scale Java modernization |
| **OpenRewrite** | Automated code transformations via composable recipes — javax→jakarta, Spring Boot 2→3 | Mechanical transformations that follow known patterns |
| **Spring Boot Migrator (SBM)** | Wraps OpenRewrite with EJB-specific recipes and a CLI | Direct EJB migration recipes (stateless beans, deployment descriptors) |
| **jscodeshift / ts-morph** | AST-level JavaScript/TypeScript code transformations | Bulk frontend code modifications (AMD→ES modules, syntax transforms) |
| **Playwright** | Visual regression testing — screenshot comparison between old and new UI | Validating that the new React UI matches the old Dojo UI |

### The pragmatic workflow

Most successful migrations combine general-purpose AI with specialized tools:

1. **AI agent** (Copilot CLI or Claude Code) for analysis, planning, and complex conversions
2. **OpenRewrite / SBM** for mechanical Java transformations (namespace changes, annotation swaps)
3. **Copilot App Modernization or Amazon Q** for Java version upgrades
4. **AI agent** again for test generation and validation

The AI agent is the orchestrator. The specialized tools are the power tools. Use both.

---

## 11. Resources

### EJB to Spring Boot

- [EJB to Spring Boot Migration Guide 2026 — LegacyLeap](https://www.legacyleap.ai/blog/ejb-to-spring-boot-migration/)
- [Converting an EJB Application to Spring Boot Using GitHub Copilot — Microsoft DevBlogs](https://devblogs.microsoft.com/all-things-azure/converting-an-ejb-application-to-spring-boot-using-github-copilot/)
- [EJB to Spring Boot: Challenges & Solutions — Medium](https://fiyas-zacharia.medium.com/ejb-to-spring-boot-migration-challenges-solutions-b4c18b0c0fec)
- [Spring Boot Migrator — GitHub (spring-projects-experimental)](https://github.com/spring-projects-experimental/spring-boot-migrator)
- [WebLogic & JBoss to Spring Boot Migration — LegacyLeap](https://www.legacyleap.ai/blog/weblogic-jboss-to-spring-boot-migration/)

### Dojo to React

- [Integrate React into Legacy Dojo Application — IBM Developer](https://developer.ibm.com/articles/migrating-existing-legacy-application-in-dojo-to-react-step-by-step-guide/)
- [Using React Instead of Dijit with Dojo Toolkit — 10Clouds](https://10clouds.com/blog/web/using-react-instead-of-dijit-with-dojo-toolkit/)
- [Migrating a UI Component from Dojo to React — DEV Community](https://dev.to/cecitorresmx/migrating-a-ui-component-from-dojojs-to-reactjs-14lg)
- [Centric Software: Dojo to TypeScript + React — SitePen Case Study](https://www.sitepen.com/case-study/centric)
- [Upgrading from Dojo to React — Mendix / Medium](https://medium.com/mendix/upgrading-from-dojo-to-react-cfc6f9a17f66)
- [dojo-in-react Wrapper — GitHub](https://github.com/Randyhuls/dojo-in-react)
- [dojo-webpack-plugin — GitHub (OpenNTF)](https://github.com/OpenNTF/dojo-webpack-plugin)

### AI-Assisted Migration

- [Claude Code for Legacy Modernization — Richard Porter](https://richardporter.dev/blog/claude-code-legacy-modernization)
- [The Code Modernization Playbook — Anthropic (PDF)](https://resources.anthropic.com/hubfs/Code%20Modernization%20Playbook.pdf)
- [How GitHub Copilot and AI Agents Are Saving Legacy Systems — GitHub Blog](https://github.blog/ai-and-ml/github-copilot/how-github-copilot-and-ai-agents-are-saving-legacy-systems/)
- [Step-by-Step Java Modernization with Copilot Agent Mode — GitHub Blog](https://github.blog/ai-and-ml/github-copilot/a-step-by-step-guide-to-modernizing-java-projects-with-github-copilot-agent-mode/)
- [AI Tools for Legacy Refactoring — Devox Software](https://devoxsoftware.com/blog/ai-tools-for-accelerating-legacy-refactoring-copilot-claude-cursor/)
- [Legacy Code Migration with ML — Augment Code](https://www.augmentcode.com/guides/legacy-code-migration-with-machine-learning-patterns-that-preserve-architecture-while-modernizing)
- [Agentic AI for Modernization — Simform](https://www.simform.com/blog/agentic-ai-for-modernization/)

### Migration Patterns

- [Strangler Fig Pattern — Microsoft Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/patterns/strangler-fig)
- [Patterns of Legacy Displacement — Martin Fowler](https://martinfowler.com/articles/patterns-legacy-displacement/)
- [Micro Frontends for Legacy Migrations — Medium](https://medium.com/@johnlawrimore/micro-frontends-a-game-changing-strategy-for-legacy-app-migrations-6288f50a6f72)
- [Incremental Migration Approaches — CircleCI](https://circleci.com/blog/incremental-migration-approaches-for-legacy-applications/)
- [Spec-Driven Frontend Migration with AI — Augment Code](https://www.augmentcode.com/guides/spec-driven-frontend-migration-with-ai-prompts)

### Anti-Patterns and Lessons Learned

- [Fantastic Rewrites and How to Avoid Them — Frontend at Scale](https://frontendatscale.com/issues/19/)
- [Top Mistakes in Legacy Software Modernization — Scalable Human](https://scalablehuman.com/2025/09/12/top-mistakes-in-legacy-software-modernization-real-experiences-revealed/)
- [Refactoring Legacy JSP Apps to React: What We Gained and What Broke — Medium](https://medium.com/@maanvik.gupta25/refactoring-legacy-jsp-apps-to-react-what-we-gained-and-what-broke-3cc74d315805)

### Case Studies

- [Amazon Q Developer Transform — 4,500 Dev-Years Saved — AWS](https://aws.amazon.com/q/developer/transform/)
- [Novacomp Java 8 to 17 with AI — AWS Case Study](https://aws.amazon.com/solutions/case-studies/novacomp-case-study/)
- [Modernizing Struts2 to Spring Boot with Claude Code — DEV Community](https://dev.to/damogallagher/modernizing-legacy-struts2-applications-with-claude-code-a-developers-journey-2ea7)
- [Vue to React with AI Agents — Money Forward](https://global.moneyforward-dev.jp/2025/06/24/how-to-utilize-ai-agents-to-accelerate-frontend-code-migration/)
- [Kenshoo: ExtJS to React Migration — Medium](https://medium.com/kenshoos-engineering-blog/should-you-migrate-fea360077aaf)
