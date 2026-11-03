# 28-Day Forward Deployed Engineer Roadmap

Oct 31, 2026 · @henry

## How this roadmap works

In 28 hours you will run one realistic client engagement end to end: messy data, an AI assistant, a secure deployment, and a demo to a non-technical customer. That is exactly what a Forward Deployed Engineer (FDE) does, and it's what most candidates can't show.

**Your fictional client:** *SwiftRoute Logistics*, a mid-size delivery company. They have messy shipment spreadsheets, PDF invoices and a support inbox full of customer complaints. Their ops manager wants to ask plain-English questions like "Which routes were late most often last week, and why?" and get trustworthy answers.

**Why one project instead of tutorials:** FDE interviews test whether you can take an unclear business problem and ship something that works in the customer's world. A single deep project with evals, deployment, a postmortem and a demo beats ten tutorial certificates.

**Daily rules**

- 1 hour, hands on keyboard. Reading docs counts only if you build with them in the same hour.
- Commit to GitHub every day, even if the change is small. A 28-day streak is visible proof of consistency.
- If a task runs over, cut scope rather than skipping it. Choosing what to drop is a core FDE skill.
- Keep a `JOURNAL.md` in the repo: 3 lines a day covering what you did, what broke, and what you decided. This becomes interview material.
- Tick each day's box below when it's done.

## Week 1: Turn messy client data into a working API

By Sunday you'll have the client's raw data cleaned and loaded into Postgres, plus an API that answers real business questions. Real customer data is never clean, and FDEs spend a large share of their time on this unglamorous step.

- [ ] **Day 1: Write the client brief and generate dirty data**
  - **Do:** Write a one-page brief: who the client is, the 3 questions the ops manager needs answered, and what "success" means (e.g. answers within 5 seconds, every answer traceable to a source). Then create about 500 shipment rows with deliberate mess: duplicates, 3 different date formats, blank cells, inconsistent city spellings ("Kozhikode" vs "Calicut"). Make 3 to 5 fake PDF invoices and 30 short support emails.
  - **Why:** FDEs start every engagement by turning a vague ask into written success criteria. Without them you can't tell the customer when you're done. Creating the mess yourself also teaches you the patterns to look for in real client data.
- [ ] **Day 2: Profile the data before cleaning it**
  - **Do:** Load the raw files into a notebook or script and list every problem: count nulls per column, find duplicates, list every distinct city spelling and date format. Write the findings as a short "data quality report" in the repo.
  - **Why:** Jumping straight into cleaning hides problems. A data quality report is something you'd actually send a client, and it shows them issues in their own systems that they didn't know about. That builds trust fast.
- [ ] **Day 3: Build the cleaning pipeline (ETL)**
  - **Do:** Write a Python script that cleans each issue from Day 2, then loads clean rows into Postgres. Rows that can't be fixed go into a `rejected_rows` table with the reason. Make the script safe to re-run without creating duplicates.
  - **Why:** Customers send new data every week, so the pipeline must be repeatable. Keeping rejected rows, rather than silently dropping them, means you can answer "where did my 37 missing shipments go?", a question every client eventually asks.
- [ ] **Day 4: Extract structured data from the PDF invoices**
  - **Do:** Pull invoice number, date, amount, route and line items out of the PDFs into a Postgres table. Try a PDF text library first, then try an LLM with a strict JSON schema, and compare which was more accurate.
  - **Why:** Unstructured documents (PDFs, scans, emails) are the main reason companies hire FDEs for AI work. Comparing a rule-based approach with an LLM teaches you when each one is the right choice, which is a common interview question.
- [ ] **Day 5: Design the API around the client's questions**
  - **Do:** List 5 endpoints that directly answer the brief, e.g. late shipments by route, cost per route, top complaint reasons, shipment detail by ID, invoice lookup. Build the first 2 in FastAPI or Express, with proper database indexes.
  - **Why:** Designing endpoints from business questions, rather than from database tables, is how FDEs think. It keeps the work tied to what the customer will pay for.
- [ ] **Day 6: Finish the API and add basic tests**
  - **Do:** Build the remaining 3 endpoints. Add input validation, clear error messages and auto-generated Swagger docs. Write one test per endpoint.
  - **Why:** In Week 2 the AI will call these endpoints as tools. If they return vague errors, the AI will give vague answers. Tests let you change things later without fear.
- [ ] **Day 7: Make it run in under 5 commands**
  - **Do:** Write a README that takes a stranger from `git clone` to a working API in 5 commands or fewer. Ask a friend to try it, or try it yourself in a fresh folder. Fix whatever broke.
  - **Why:** FDEs hand systems over to customer engineers who've never seen them. If setup is painful, the project dies after you leave. Recruiters also judge repos by the README first.

## Week 2: Add the AI layer, and prove it works

By Sunday the ops manager can ask questions in plain English and get answers that cite their sources, with a score showing how often the AI is right. The scoring (evals) is what separates FDEs from people who just built a chatbot.

- [ ] **Day 8: Make the documents searchable by meaning (embeddings)**
  - **Do:** Split the invoices and support emails into small chunks, create embeddings for each chunk, and store them in Postgres using the pgvector extension. Test by searching "customer angry about late delivery" and checking whether the right emails come back.
  - **Why:** This is the retrieval half of RAG (retrieval-augmented generation). If the wrong chunks are retrieved, no prompt can fix the answer. Using pgvector inside your existing Postgres instead of a separate vector database is also a choice clients like, because it means one less system to run.
- [ ] **Day 9: Build question-answering with citations (RAG)**
  - **Do:** When a question comes in, retrieve the top chunks, send them to an LLM with the question, and require the answer to cite which email or invoice each claim came from. If nothing relevant is found, the AI must say "I don't know".
  - **Why:** Enterprise clients don't trust answers they can't verify. Citations, plus a refusal to guess, are what make an AI tool acceptable to a real ops team.
- [ ] **Day 10: Let the AI call your API (tool calling)**
  - **Do:** Expose your 5 Week 1 endpoints to the LLM as tools, each with a clear name and description. Ask "Which route had the most late shipments last week?" and watch it choose and call the right endpoint.
  - **Why:** Numbers should come from the database, not from the AI's guess. Tool calling is how modern AI agents take real actions in a customer's systems, and it's the core skill in most current FDE job descriptions.
- [ ] **Day 11: Combine both into one assistant**
  - **Do:** Build one assistant that decides whether a question needs documents (RAG), data (tools), or both. Example: "Why were Kozhikode deliveries late?" needs late-shipment numbers from the API plus complaint reasons from the emails.
  - **Why:** Real questions mix structured and unstructured data. Handling both in one flow is what makes the demo feel like magic to a client.
- [ ] **Day 12: Write evals (your AI's test suite)**
  - **Do:** Write 20 test questions with the expected answer and expected source for each. Include 5 tricky ones: ambiguous questions, questions with no answer in the data, and one that tries to trick the AI. Write a script that runs all 20 and prints a score.
  - **Why:** "It seems to work" is not acceptable to a paying customer. A score lets you say "accuracy went from 60% to 85%", which is the kind of sentence that gets you hired.
- [ ] **Day 13: Fix your 3 worst failures and re-measure**
  - **Do:** Look at failed eval questions and find the cause of each: bad retrieval, bad prompt, bad tool description, or bad data. Fix the 3 worst, re-run the evals, and record the before and after score in your journal.
  - **Why:** Diagnosing why an AI failed is the daily work of an FDE. Being able to explain a specific failure and how you fixed it is one of the strongest interview stories you can have.
- [ ] **Day 14: Build a simple chat screen**
  - **Do:** Make a minimal Next.js page: a chat box, answers with clickable source links, and a loading state. Keep it plain; don't spend time on styling.
  - **Why:** Customers judge the whole system by what they can see. A working screen also turns your project into something you can demo in 2 minutes, which you'll need in Week 4.

## Week 3: Deploy it as if it's going into the customer's environment

By Sunday the system is live on AWS with login, monitoring, automated checks and safety guardrails. A demo on your laptop impresses no one; a secure, observable deployment is what clients actually sign off on.

- [ ] **Day 15: Containerise everything**
  - **Do:** Put the API, the frontend and Postgres (with pgvector) into Docker Compose. Move every secret and setting into environment variables, so nothing sensitive is hard-coded. Confirm the whole stack starts with one command.
  - **Why:** Every customer's environment is different. Containers make your system portable, so it runs the same on your laptop, on AWS, or on the client's own servers.
- [ ] **Day 16: Deploy to AWS with HTTPS**
  - **Do:** Deploy to an EC2 instance (or ECS if you're comfortable), put Nginx in front, and add a free HTTPS certificate. Write down every manual step you took in a `DEPLOY.md`.
  - **Why:** FDEs often deploy into infrastructure they don't control. Writing the steps down shows you what to automate next and gives the client's team a way to redeploy without you.
- [ ] **Day 17: Add login and permissions**
  - **Do:** Add Google OAuth login. Create 2 roles: "ops" users see shipments and answers; "admin" users can also see costs and invoice amounts. Make sure the AI also respects these roles, so an ops user can't ask it for invoice totals.
  - **Why:** The first question any enterprise security team asks is "who can see what?" Making the AI respect permissions is a problem many AI demos ignore, and solving it puts you ahead of most candidates.
- [ ] **Day 18: Add monitoring (observability)**
  - **Do:** Add OpenTelemetry tracing so you can see each request's path: question, retrieval, tool calls, LLM call, answer. Log the time taken and the LLM cost for every question. Build a simple view of the slowest and most expensive questions.
  - **Why:** When a client says "the AI was slow and wrong yesterday at 3pm", you need to see exactly what happened. Cost tracking matters too: clients will ask what this costs per month before approving it.
- [ ] **Day 19: Break it on purpose and write a postmortem**
  - **Do:** Cause a realistic failure: stop the database, push a broken config, or use an expired API key. Use your monitoring to find and fix it. Write a 1-page postmortem: what happened, how you noticed, the root cause, the fix, and how to stop it happening again.
  - **Why:** Things break in production, and FDEs are often the first ones called. A calm, written postmortem is a senior-engineer habit, and it's an excellent document to show in interviews.
- [ ] **Day 20: Automate checks with CI**
  - **Do:** Set up GitHub Actions to run your API tests and your 20 evals on every push. Make the build fail if the eval score drops below your current level.
  - **Why:** Changing a prompt to fix one question can quietly break five others. Running evals automatically is how serious AI teams prevent this, and few candidates have it set up.
- [ ] **Day 21: Add safety guardrails**
  - **Do:** Add 3 protections: detect and block prompt-injection attempts hidden inside emails (e.g. an email saying "ignore your instructions"); mask phone numbers and emails in answers; add a rate limit per user. Add 3 eval questions that test these.
  - **Why:** Customer data often contains text the AI shouldn't obey or reveal. Showing you've thought about AI security makes clients, and interviewers, trust you with real systems.

## Week 4: The customer-facing half most engineers skip

By Sunday you can demo, explain, adapt and interview like an FDE. Half the job is talking to customers, and this is where most strong engineers fall short.

- [ ] **Day 22: Handle a surprise requirement change**
  - **Do:** Pretend the client emails: "We also need data from our new warehouse system," with a new CSV in a different format. Add it to the pipeline, the API and the AI within 1 hour. Time yourself and note what slowed you down.
  - **Why:** Requirements change mid-project on every real engagement. Speed of adaptation is the skill FDE interviewers probe most, and this gives you a true story to tell.
- [ ] **Day 23: Record a demo for a non-technical manager**
  - **Do:** Record a 5-minute screen video for the ops manager. Start with their problem, show 3 real questions being answered, show a source being checked, and end with the eval score and monthly cost. Don't mention frameworks or code.
  - **Why:** Customers buy outcomes, not architecture. Explaining technical work in business language is the skill that most separates FDEs from regular backend engineers. The video doubles as portfolio material.
- [ ] **Day 24: Write a technical design doc**
  - **Do:** Write 1 to 2 pages for the client's engineering team: an architecture diagram, why you chose each component (e.g. pgvector over a separate vector DB), the trade-offs, known limitations, and what you'd build next with more time.
  - **Why:** FDEs leave systems behind for others to run. A clear design doc shows you think beyond code, and it's ready-made material for system design interviews.
- [ ] **Day 25: Practise scoping a new problem out loud**
  - **Do:** Pick a business problem you haven't worked on, e.g. "A hospital wants AI to summarise patient discharge notes." In 45 minutes, talking out loud, list your questions for the client, the risks, a 2-week MVP, and how you'd measure success. Record yourself and listen back.
  - **Why:** FDE interviews often include a "customer case" round with an unclear problem. Practising the structure (questions, then risks, then MVP, then metrics) makes it automatic under pressure.
- [ ] **Day 26: Live-debugging drill**
  - **Do:** Ask Claude or a friend to plant 2 hidden bugs in a copy of your repo without telling you where. Find and fix them while explaining your reasoning out loud, as if a customer is watching on a call.
  - **Why:** FDEs often debug live in front of customers. Staying calm and narrating your thinking clearly is a learnable skill, and interviews test it directly.
- [ ] **Day 27: Turn the project into resume and LinkedIn material**
  - **Do:** Write 3 to 4 resume bullets with real numbers from your journal: eval accuracy before and after, response time, cost per question, time taken to add the new data source. Pin the repo on GitHub, and post a short LinkedIn write-up with the demo video.
  - **Why:** Numbers make claims believable. Recruiters spend seconds on a resume, and a pinned, documented project with a demo video tells your story without an interview.
- [ ] **Day 28: Full mock FDE interview**
  - **Do:** Run a 60-minute mock covering: a 15-minute walkthrough of your project, a 20-minute customer roleplay (an unhappy client says the AI gave a wrong answer), and a 25-minute system design question. Claude can play the interviewer. Write down your 3 weakest moments.
  - **Why:** This shows you exactly where you stand and what to practise in week 5. Your 3 weakest moments become your next study plan.

## What you'll have after Day 28

These 8 pieces of proof are what put you ahead of most FDE applicants, who typically show only tutorials or a basic chatbot.

| Proof | Where it lives | What it shows an interviewer |
| --- | --- | --- |
| Data quality report + ETL with rejected rows | GitHub repo | You can handle real, messy customer data |
| RAG + tool-calling assistant with citations | Live AWS URL | You can build trustworthy AI, not just a chatbot |
| Eval suite with before/after scores | Repo + CI | You measure quality instead of guessing |
| Login, role-based access, guardrails | Live app | You think about enterprise security |
| Tracing and cost tracking | Live app | You can run and debug AI in production |
| Incident postmortem | Repo | You handle failure calmly and professionally |
| 5-minute demo video + design doc | LinkedIn, repo | You can explain technical work to customers |
| 28-day commit streak + journal | GitHub | You are consistent and reflective |

An honest note: 28 hours alone won't make you a top-30% FDE. Your 3+ years of full-stack experience plus this complete, measured, deployed project will put you ahead of most candidates, because most never get past the demo stage.
