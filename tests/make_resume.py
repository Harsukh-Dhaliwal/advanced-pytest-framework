import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Initialize Document with clean margins for linear layout
pdf_path = "Harsukh_Dhaliwal_ATS_Optimized_Resume.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=50, rightMargin=50, topMargin=45, bottomMargin=45,
    title="Harsukh Dhaliwal - QA Automation Engineer Resume"
)

styles = getSampleStyleSheet()
story = []

PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep Slate Blue
TEXT_COLOR = colors.HexColor("#2D3748")      # Charcoal

# Typography Styling tailored for clean ATS string extraction
styles.add(ParagraphStyle(name='DocTitle', fontName='Helvetica-Bold', fontSize=20, leading=24, textColor=PRIMARY_COLOR, alignment=1))
styles.add(ParagraphStyle(name='ContactInfo', fontName='Helvetica', fontSize=9, leading=13, textColor=TEXT_COLOR, alignment=1))
styles.add(ParagraphStyle(name='SectionHeading', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=PRIMARY_COLOR, spaceBefore=10, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name='BodyBoldCustom', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=TEXT_COLOR))
styles.add(ParagraphStyle(name='BodyTextCustom', fontName='Helvetica', fontSize=9.5, leading=13, textColor=TEXT_COLOR))
styles.add(ParagraphStyle(name='BulletTextCustom', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=TEXT_COLOR, leftIndent=12, firstLineIndent=-12, spaceAfter=2.5))

# Header Block
story.append(Paragraph("HARSUKH DHALIWAL", styles['DocTitle']))
story.append(Paragraph("Brampton, ON | 289-952-9329 | harsukhd2002@gmail.com | https://github.com", styles['ContactInfo']))
story.append(Spacer(1, 4))

# 1. Technical Profile Section
story.append(Paragraph("TECHNICAL SKILLS", styles['SectionHeading']))
story.append(Paragraph("<b>Languages & Core Engines:</b> Python, SQL (SQLite), HTML5, CSS3, JavaScript, Shell Scripting", styles['BodyTextCustom']))
story.append(Paragraph("<b>Automation Frameworks & Engineering Tools:</b> Pytest, Playwright (Sync/Async API), Locust Load Engine, Docker Containers, Selenium WebDriver, Automation Engineering", styles['BodyTextCustom']))
story.append(Paragraph("<b>Architecture, SDLC & Testing Patterns:</b> Page Object Model (POM), Database Test Parameterization, Relational Mapping, Concurrency Performance Testing, API Interception, Backend API Mocking, Data-Driven Testing, Regression Testing, Manual Testing, Software Development Life Cycle (SDLC)", styles['BodyTextCustom']))
story.append(Paragraph("<b>DevOps, Infrastructure & Systems:</b> GitHub Actions, CI/CD Cloud Pipelines, Linux (Ubuntu Virtual Nodes), Environment Virtualization, Git Version Control, VS Code, Thread Isolation (pytest-xdist)", styles['BodyTextCustom']))

# 2. Portfolio Project Section
story.append(Paragraph("QA AUTOMATION PROJECT CENTERPIECE", styles['SectionHeading']))
story.append(Paragraph("<b>Lead SDET & Framework Architect</b> | Open-Source Git Portfolio Project", styles['BodyBoldCustom']))
story.append(Paragraph("<i>Enterprise Hybrid UI, API & Performance Test Automation Platform Framework</i>", styles['BodyTextCustom']))
story.append(Spacer(1, 3))
story.append(Paragraph("- <b>Engineered Modular Page Object Models (POM):</b> Decoupled web DOM paths from testing logic using object-oriented Python classes, cutting functional suite maintenance overhead by 50%.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Implemented Isolated Browser-Level API Mocking:</b> Architected offline test routing wrappers via browser tab network context intercepts, defeating environment network latency to achieve fast, isolated execution loops.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Orchestrated Concurrent Multi-Worker Execution Pipelines:</b> Integrated pytest-xdist to slash test suite runtimes by over 60%; isolated process logs using PYTEST_XDIST_WORKER variables to eliminate multi-threaded file-locking race conditions.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Resolved Cross-Browser Synchronicity Constraints:</b> Configured a native validation matrix targeting Chromium, Firefox, and WebKit; engineered explicit actionability wait state handling (wait_for) to defeat asynchronous layout rendering delays.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Engineered High-Concurrency Load Simulation Engines (Option K):</b> Developed an independent performance testing suite using Locust to simulate multi-tenant user traffic metrics and isolate systemic backend latency bottlenecks.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Architected Containerized Environment Sandbox Isolation (Option L):</b> Authored custom Dockerfile configurations to fully package dependencies, python host runtimes, and headless browser binaries into virtualization containers.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Designed Relational Test Data Persistence Layers (Option M):</b> Programmed data-driven parameter layers mapping dynamic target test attributes out of local SQLite database files using relational query configurations.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Constructed Data-Driven Report Configurations:</b> Structured a secure framework utilizing externalized datasets alongside custom HTML reporting engines containing automated screenshot capture hooks on test failure events.", styles['BulletTextCustom']))
story.append(Paragraph("- <b>Orchestrated GitHub Actions Cloud Pipelines:</b> Formulated automated branch-tracking workflows (main.yml) that auto-provision clean virtual nodes, install package environments, pull web browsers, and push live build status telemetry webhooks.", styles['BulletTextCustom']))

# 3. Professional Experience Section
story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['SectionHeading']))
story.append(Paragraph("<b>Logistics Operator & Client Service Specialist</b> | Independent Contractor | 2020 – Present", styles['BodyBoldCustom']))
story.append(Paragraph("- Systematically audited high-volume inventory accuracy and tracked logistical transport data parameters prior to routing, maintaining a 100% precision and compliance rate across thousands of client data packets.", styles['BulletTextCustom']))
story.append(Paragraph("- Leveraged on-the-spot technical hardware troubleshooting and critical thinking to resolve systemic delivery constraints, preserving top-tier client safety metrics.", styles['BulletTextCustom']))

story.append(Spacer(1, 3))
story.append(Paragraph("<b>Operations Crew Member</b> | Wendy's | May 2022 – Oct 2022", styles['BodyBoldCustom']))
story.append(Paragraph("- Executed rapid point-of-sale (POS) financial transaction entries and data transfers with extreme accuracy under strict, fast-paced time constraints.", styles['BulletTextCustom']))
story.append(Paragraph("- Coordinated with cross-functional service teams to monitor operational workflows and uphold stringent quality control and visual inventory hygiene benchmarks.", styles['BulletTextCustom']))

story.append(Spacer(1, 3))
story.append(Paragraph("<b>Office Assistant</b> | Woodwal Law Office | Feb 2019 – Jun 2019", styles['BodyBoldCustom']))
story.append(Paragraph("- Managed the systematic entry, categorization, and secure indexing of physical and digital business files into reference databases, maintaining data integrity with zero discrepancies.", styles['BulletTextCustom']))

# 4. Education Section
story.append(Paragraph("EDUCATION & COMPUTER SCIENCE BACKGROUND", styles['SectionHeading']))
story.append(Paragraph("<b>Bachelor of Science Coursework (Computer Science Focus)</b> | 2021 – 2023", styles['BodyBoldCustom']))
story.append(Paragraph("<i>Wilfrid Laurier University – Waterloo, ON</i>", styles['BodyTextCustom']))
story.append(Spacer(1, 2))
story.append(Paragraph("- Completed intensive academic fundamentals in core Object-Oriented Programming (OOP) architectures, function layouts, condition execution loops, script logic syntax, and programmatic problem-solving.", styles['BulletTextCustom']))

doc.build(story)
print("SUCCESS: Harsukh_Dhaliwal_ATS_Optimized_Resume.pdf has been generated successfully with complete Option K-M milestones!")