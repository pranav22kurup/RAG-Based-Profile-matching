"""
Generate 30+ diverse synthetic resumes for RAG system testing.
"""
import os
import random

random.seed(42)

RESUMES = [
    {
        "name": "Alice Chen",
        "file": "alice_chen.txt",
        "content": """ALICE CHEN
alice.chen@email.com | (415) 555-0101 | San Francisco, CA | linkedin.com/in/alicechen

SUMMARY
Senior Machine Learning Engineer with 7 years of experience building production ML systems. 
Expert in deep learning, NLP, and MLOps. Led teams of 5+ engineers at top tech companies.

EXPERIENCE

Senior ML Engineer | Google DeepMind | 2020 – Present
- Designed and deployed large-scale NLP models serving 100M+ daily users
- Built distributed training pipelines using PyTorch and JAX on TPU clusters
- Reduced model inference latency by 40% through quantization and distillation
- Mentored 4 junior engineers; led weekly ML reading groups

ML Engineer | Uber AI | 2018 – 2020
- Developed real-time fraud detection model (XGBoost + LSTM) saving $50M annually
- Built feature store serving 500+ ML features to 20+ teams
- Implemented A/B testing framework for model evaluation

Data Scientist | Airbnb | 2016 – 2018
- Created dynamic pricing model increasing host revenue by 12%
- Built recommendation engine using collaborative filtering (ALS)

EDUCATION
M.S. Computer Science (Machine Learning) | Stanford University | 2016
B.S. Mathematics & Statistics | UC Berkeley | 2014

SKILLS
Languages: Python, Scala, SQL, C++
ML/DL: PyTorch, TensorFlow, JAX, scikit-learn, Hugging Face Transformers
MLOps: Kubeflow, MLflow, Airflow, Docker, Kubernetes
Cloud: GCP (Vertex AI), AWS (SageMaker), Azure ML
Specialties: NLP, Computer Vision, Reinforcement Learning, LLMs

PUBLICATIONS
- "Efficient Fine-Tuning of Large Language Models" – NeurIPS 2022
- "Scalable Fraud Detection with Graph Neural Networks" – KDD 2020
"""
    },
    {
        "name": "Bob Martinez",
        "file": "bob_martinez.txt",
        "content": """BOB MARTINEZ
bob.martinez@email.com | (512) 555-0202 | Austin, TX

SUMMARY
Full-Stack Software Engineer with 5 years experience in React, Node.js, and cloud infrastructure. 
Passionate about building scalable web applications and developer tooling.

EXPERIENCE

Senior Software Engineer | Stripe | 2021 – Present
- Built payment dashboard used by 2M+ merchants using React and TypeScript
- Designed REST and GraphQL APIs handling 10M+ requests/day
- Led migration from monolith to microservices, reducing deployment time by 60%

Software Engineer | Indeed | 2019 – 2021
- Developed job recommendation engine serving 250M users
- Optimized PostgreSQL queries reducing p99 latency from 800ms to 120ms
- Built CI/CD pipelines using GitHub Actions and Terraform

Junior Developer | Dell Technologies | 2018 – 2019
- Created internal HR portal using Angular and .NET Core
- Wrote automated test suites increasing code coverage from 40% to 85%

EDUCATION
B.S. Computer Science | University of Texas at Austin | 2018

SKILLS
Frontend: React, TypeScript, Next.js, Vue.js, HTML/CSS
Backend: Node.js, Python, Go, Java, .NET Core
Databases: PostgreSQL, MongoDB, Redis, Elasticsearch
DevOps: AWS, Docker, Kubernetes, Terraform, Jenkins
Testing: Jest, Cypress, Selenium

PROJECTS
- Open-source React component library (1.2k GitHub stars)
- Personal finance tracker app (5,000+ active users)
"""
    },
    {
        "name": "Carol Johnson",
        "file": "carol_johnson.txt",
        "content": """CAROL JOHNSON
carol.johnson@email.com | (212) 555-0303 | New York, NY

SUMMARY
Data Engineer with 6 years of experience designing and maintaining large-scale data pipelines.
Expert in Spark, Kafka, and cloud data warehousing. Strong background in data modeling.

EXPERIENCE

Senior Data Engineer | JPMorgan Chase | 2021 – Present
- Architected real-time risk analytics platform processing 5TB/day using Apache Kafka and Spark Streaming
- Built data lakehouse on AWS (S3 + Delta Lake) replacing legacy Oracle data warehouse
- Reduced data pipeline failures by 70% through robust monitoring with DataDog and PagerDuty
- Designed dimensional data models for regulatory reporting (Basel III compliance)

Data Engineer | Bloomberg LP | 2018 – 2021
- Maintained ETL pipelines for financial market data across 150+ exchanges
- Migrated on-premise Hadoop cluster to GCP (Dataproc + BigQuery), saving $2M/year
- Built self-service data catalog using Apache Atlas

Data Analyst | Deloitte | 2017 – 2018
- Created Power BI dashboards for Fortune 500 client analytics
- Automated Excel-based reporting with Python, saving 20 hours/week

EDUCATION
M.S. Data Science | Columbia University | 2017
B.S. Statistics | NYU Stern School of Business | 2015

SKILLS
Languages: Python, Scala, SQL, Java
Big Data: Apache Spark, Kafka, Flink, Hadoop, Hive
Cloud: AWS (Glue, EMR, Redshift), GCP (BigQuery, Dataflow), Azure Synapse
Databases: PostgreSQL, Snowflake, Delta Lake, Cassandra
Orchestration: Airflow, Prefect, dbt
"""
    },
    {
        "name": "David Kim",
        "file": "david_kim.txt",
        "content": """DAVID KIM
david.kim@email.com | (206) 555-0404 | Seattle, WA

SUMMARY
DevOps / Platform Engineer with 8 years experience in cloud infrastructure, Kubernetes, and SRE practices. 
Built and managed infrastructure for systems handling millions of concurrent users.

EXPERIENCE

Staff Platform Engineer | Amazon Web Services | 2019 – Present
- Designed multi-region Kubernetes platform serving 500+ internal engineering teams
- Led SRE practices achieving 99.99% uptime SLA for critical payment services
- Built infrastructure-as-code frameworks (Terraform + CDK) adopted by 200+ teams
- Reduced cloud costs by $8M/year through resource optimization and spot instance strategies

Senior DevOps Engineer | Microsoft | 2016 – 2019
- Managed Azure DevOps pipelines for Office 365 (1B+ users)
- Implemented GitOps workflows with ArgoCD and Flux
- Built chaos engineering platform for resiliency testing

Systems Engineer | Boeing | 2015 – 2016
- Administered Linux server fleet (500+ nodes) and network infrastructure

EDUCATION
B.S. Electrical Engineering | University of Washington | 2015

SKILLS
Cloud: AWS (expert), GCP, Azure
Container Orchestration: Kubernetes, Docker, Helm, Istio
IaC: Terraform, Pulumi, AWS CDK, Ansible, Chef
CI/CD: GitHub Actions, Jenkins, CircleCI, ArgoCD
Monitoring: Prometheus, Grafana, Datadog, ELK Stack
Languages: Python, Go, Bash, TypeScript

CERTIFICATIONS
AWS Solutions Architect Professional | CKA (Kubernetes) | GCP Professional Cloud Architect
"""
    },
    {
        "name": "Emma Williams",
        "file": "emma_williams.txt",
        "content": """EMMA WILLIAMS
emma.williams@email.com | (617) 555-0505 | Boston, MA

SUMMARY
Product Manager with 6 years experience leading data-driven product strategy at B2B SaaS companies.
Strong technical background with experience in ML product development and API platforms.

EXPERIENCE

Senior Product Manager | HubSpot | 2021 – Present
- Owned CRM AI features roadmap; launched 3 ML-powered features generating $15M ARR
- Led cross-functional team of 12 (engineering, design, data science)
- Defined product metrics and ran 50+ A/B experiments to optimize conversion funnels
- Reduced customer churn by 18% through predictive churn modeling product

Product Manager | Klaviyo | 2018 – 2021
- Launched email deliverability dashboard increasing customer satisfaction (NPS +22)
- Managed integrations ecosystem with 200+ partners (Shopify, Salesforce, etc.)
- Wrote detailed PRDs and user stories; facilitated sprint planning

Associate PM | Wayfair | 2017 – 2018
- Supported search and discovery team; conducted user research with 100+ customers

EDUCATION
MBA | Harvard Business School | 2017
B.S. Computer Science | MIT | 2015

SKILLS
Product: Roadmapping, PRD Writing, A/B Testing, User Research, OKRs
Technical: SQL, Python (basic), API design, data analysis
Tools: JIRA, Figma, Amplitude, Mixpanel, Looker, Tableau
Methodologies: Agile/Scrum, Design Thinking, Jobs-to-be-Done
"""
    },
    {
        "name": "Frank Nguyen",
        "file": "frank_nguyen.txt",
        "content": """FRANK NGUYEN
frank.nguyen@email.com | (408) 555-0606 | San Jose, CA

SUMMARY
Backend Software Engineer with 4 years of experience specializing in distributed systems and API development.
Expert in Java, Go, and microservices architecture. Experience with high-throughput financial systems.

EXPERIENCE

Software Engineer II | PayPal | 2022 – Present
- Built payment processing microservices handling $500M in daily transactions
- Designed gRPC APIs with 99.99% availability using Circuit Breaker patterns
- Implemented event-driven architecture with Apache Kafka for audit logging
- Improved API response time by 35% through caching with Redis

Software Engineer | Cisco | 2020 – 2022
- Developed network configuration management APIs using Spring Boot and Java
- Built automated testing framework reducing QA cycle from 2 weeks to 3 days
- Contributed to open-source networking libraries

EDUCATION
B.S. Computer Engineering | UC Santa Clara | 2020

SKILLS
Languages: Java (expert), Go, Python, SQL
Frameworks: Spring Boot, Gin, gRPC, REST
Databases: PostgreSQL, MySQL, Redis, Cassandra
Messaging: Apache Kafka, RabbitMQ
Cloud: AWS, GCP, Docker, Kubernetes
Testing: JUnit, Mockito, TestContainers
"""
    },
    {
        "name": "Grace Park",
        "file": "grace_park.txt",
        "content": """GRACE PARK
grace.park@email.com | (310) 555-0707 | Los Angeles, CA

SUMMARY
UX/UI Designer with 5 years experience creating intuitive digital experiences for mobile and web.
Specializes in design systems, accessibility, and data visualization. Strong user research skills.

EXPERIENCE

Senior UX Designer | Netflix | 2021 – Present
- Redesigned content discovery experience for 230M+ subscribers (increased engagement 25%)
- Led design system initiative; created 200+ reusable components
- Conducted 80+ user interviews and usability studies
- Collaborated with 15 engineering teams to ensure pixel-perfect implementation

UX Designer | Hulu | 2019 – 2021
- Designed streaming player UI for smart TVs, web, and mobile
- Created accessibility improvements achieving WCAG 2.1 AA compliance
- Ran A/B tests on onboarding flow reducing drop-off by 30%

Junior Designer | IDEO | 2018 – 2019
- Contributed to design sprints for Fortune 500 clients in healthcare and fintech

EDUCATION
M.F.A. Interaction Design | ArtCenter College of Design | 2018
B.A. Psychology | UCLA | 2016

SKILLS
Design: Figma, Sketch, Adobe XD, InVision, Prototyping, Wireframing
Research: Usability testing, User interviews, Journey mapping, Card sorting
Technical: HTML/CSS, basic JavaScript, iOS/Android guidelines
Specialties: Design systems, Accessibility (WCAG), Data visualization, Motion design
"""
    },
    {
        "name": "Henry Liu",
        "file": "henry_liu.txt",
        "content": """HENRY LIU
henry.liu@email.com | (650) 555-0808 | Menlo Park, CA

SUMMARY
AI Research Scientist with PhD and 3 years industry experience. 
Published 8 papers in top ML venues (NeurIPS, ICML, ICLR). 
Expert in reinforcement learning, large language models, and AI safety.

EXPERIENCE

Research Scientist | OpenAI | 2022 – Present
- Contributed to GPT-4 pretraining and RLHF fine-tuning pipelines
- Published research on scalable reward modeling for RLHF
- Built evaluation frameworks for LLM alignment and safety properties

Research Intern | Google Brain | 2021
- Developed novel exploration strategy for sparse-reward RL environments
- Paper accepted at NeurIPS 2021

EDUCATION
Ph.D. Computer Science (Machine Learning) | Carnegie Mellon University | 2022
B.S. Mathematics & CS | Caltech | 2017

SKILLS
Research Areas: Reinforcement Learning, LLMs, AI Safety, RLHF, Multi-agent systems
Languages: Python, C++, CUDA
Frameworks: PyTorch, JAX, TensorFlow
Math: Optimization, Probability theory, Linear algebra, Game theory

PUBLICATIONS (Selected)
- "Scalable Reward Modeling for RLHF" – NeurIPS 2023
- "Safe Exploration in Deep RL" – ICML 2022
- "Emergent Communication in Multi-Agent RL" – ICLR 2021
"""
    },
    {
        "name": "Isabella Torres",
        "file": "isabella_torres.txt",
        "content": """ISABELLA TORRES
isabella.torres@email.com | (305) 555-0909 | Miami, FL

SUMMARY
Cybersecurity Engineer with 6 years of experience in penetration testing, incident response, and security architecture.
CISSP and CEH certified. Led security programs at financial institutions and healthcare companies.

EXPERIENCE

Senior Security Engineer | Citibank | 2021 – Present
- Led red team operations discovering 40+ critical vulnerabilities before exploitation
- Architected zero-trust security model for hybrid cloud environment
- Built SIEM platform (Splunk) processing 50B+ security events/day
- Managed incident response team; reduced MTTR from 4 hours to 45 minutes

Security Engineer | Humana | 2018 – 2021
- Performed penetration tests on 200+ web applications and APIs
- Implemented HIPAA-compliant security controls for healthcare data systems
- Developed security awareness training program (2,000+ employees)

Security Analyst | Mandiant | 2017 – 2018
- Investigated APT intrusions for Fortune 500 clients
- Performed malware analysis and threat intelligence research

EDUCATION
B.S. Information Security | Florida International University | 2017

SKILLS
Offensive: Penetration testing, Burp Suite, Metasploit, Kali Linux, Social engineering
Defensive: SIEM (Splunk, IBM QRadar), EDR (CrowdStrike), IDS/IPS, WAF
Cloud Security: AWS Security Hub, Azure Sentinel, GCP Security Command Center
Compliance: HIPAA, PCI-DSS, SOC 2, NIST, ISO 27001
Languages: Python, Bash, PowerShell

CERTIFICATIONS: CISSP | CEH | OSCP | AWS Security Specialty
"""
    },
    {
        "name": "James Brown",
        "file": "james_brown.txt",
        "content": """JAMES BROWN
james.brown@email.com | (312) 555-1010 | Chicago, IL

SUMMARY
Data Scientist with 5 years of experience in statistical modeling, machine learning, and business analytics.
Strong domain expertise in retail and supply chain optimization. Expert in Python and R.

EXPERIENCE

Senior Data Scientist | Walgreens | 2021 – Present
- Built demand forecasting model (LSTM + Prophet) reducing inventory waste by 22%
- Developed customer lifetime value model optimizing marketing spend ($200M budget)
- Created automated reporting pipeline delivering insights to C-suite weekly
- Led data science team of 3, driving quarterly roadmap planning

Data Scientist | Grubhub | 2019 – 2021
- Designed dynamic pricing algorithm increasing marketplace GMV by 8%
- Built ETAs prediction model (ensemble methods) improving accuracy by 15%
- Conducted causal inference studies for marketing attribution

Analytics Engineer | Accenture | 2018 – 2019
- Built financial analytics dashboards for banking clients using Tableau and SQL

EDUCATION
M.S. Applied Statistics | University of Chicago | 2018
B.S. Mathematics | Northwestern University | 2016

SKILLS
Languages: Python, R, SQL
ML: scikit-learn, XGBoost, LightGBM, statsmodels, Prophet
Deep Learning: TensorFlow, Keras
Visualization: Tableau, Power BI, matplotlib, seaborn, Plotly
Statistical Methods: Regression, Time series, A/B testing, Causal inference, Bayesian methods
"""
    },
    {
        "name": "Katherine Lee",
        "file": "katherine_lee.txt",
        "content": """KATHERINE LEE
katherine.lee@email.com | (206) 555-1111 | Seattle, WA

SUMMARY
Cloud Architect with 10 years of experience designing enterprise-scale AWS and Azure solutions.
AWS Solutions Architect Professional and Azure Solutions Architect Expert certified.
Specialized in cloud migration, cost optimization, and well-architected frameworks.

EXPERIENCE

Principal Cloud Architect | Microsoft | 2019 – Present
- Led cloud strategy for 50+ enterprise clients migrating to Azure (avg $10M+ workloads)
- Designed globally distributed architecture for Fortune 100 retail client (3-region active-active)
- Developed Azure landing zone accelerator used by 300+ customers
- Saved clients average 35% on cloud costs through FinOps best practices

Senior Cloud Architect | Deloitte | 2016 – 2019
- Architected HIPAA-compliant cloud infrastructure for major health insurer
- Led AWS migration for financial services firm, achieving PCI-DSS compliance
- Delivered 20+ cloud architecture workshops and training sessions

Systems Engineer | HP | 2013 – 2016
- Managed on-premise data center infrastructure (1,000+ servers)

EDUCATION
B.S. Computer Science | University of Michigan | 2013

SKILLS
Cloud Platforms: AWS (expert), Azure (expert), GCP
Architecture: Microservices, Serverless, Event-driven, Multi-cloud
IaC: Terraform, ARM/Bicep, AWS CDK, CloudFormation
Networking: VPC design, DNS, CDN, VPN, Direct Connect
Security: IAM, KMS, WAF, Zero Trust
CERTIFICATIONS: AWS SA Professional | Azure SA Expert | GCP Professional | TOGAF
"""
    },
    {
        "name": "Liam O'Connor",
        "file": "liam_oconnor.txt",
        "content": """LIAM O'CONNOR
liam.oconnor@email.com | (415) 555-1212 | San Francisco, CA

SUMMARY
Mobile Engineer (iOS/Android) with 6 years of experience building consumer apps with millions of downloads.
Expert in Swift, Kotlin, and React Native. Strong focus on performance and user experience.

EXPERIENCE

Senior iOS Engineer | Lyft | 2021 – Present
- Led development of driver app used by 1M+ drivers daily (Swift, SwiftUI)
- Reduced app startup time by 50% through lazy loading and optimization
- Built real-time mapping features using MapKit and custom rendering
- Mentored 3 junior iOS engineers; led architectural decisions

Mobile Engineer | Snapchat | 2018 – 2021
- Developed AR features (Lenses) for iOS platform (50M+ daily active users)
- Integrated ML models on-device using Core ML and Metal
- Optimized memory usage reducing crashes by 40%

Junior Developer | Yelp | 2017 – 2018
- Built restaurant discovery features for iOS app (35M MAU)

EDUCATION
B.S. Computer Science | University of Southern California | 2017

SKILLS
iOS: Swift, SwiftUI, UIKit, Core Data, Core ML, ARKit, MapKit
Android: Kotlin, Jetpack Compose, Coroutines, Room
Cross-platform: React Native, Flutter
Tools: Xcode, Android Studio, Instruments, Fastlane, Firebase
Architecture: MVVM, Clean Architecture, Combine/RxSwift
"""
    },
    {
        "name": "Maria Gonzalez",
        "file": "maria_gonzalez.txt",
        "content": """MARIA GONZALEZ
maria.gonzalez@email.com | (713) 555-1313 | Houston, TX

SUMMARY
Quantitative Analyst / Algorithmic Trader with 7 years of experience in systematic trading and risk management.
Expert in Python, C++, and quantitative finance. Built trading strategies generating $50M+ alpha annually.

EXPERIENCE

Senior Quantitative Analyst | Goldman Sachs | 2020 – Present
- Developed high-frequency market-making strategies (C++, Python) with Sharpe ratio > 3.0
- Built statistical arbitrage models across equity, futures, and FX markets
- Designed risk management systems monitoring $5B portfolio in real-time
- Led team of 4 quants on systematic macro strategy development

Quantitative Researcher | Two Sigma | 2017 – 2020
- Researched and implemented ML-based alpha signals using alternative data
- Built backtesting framework in Python supporting 1000+ strategy variations/day
- Reduced signal decay through adaptive learning algorithms

EDUCATION
Ph.D. Financial Mathematics | University of Chicago | 2017
B.S. Physics | MIT | 2012

SKILLS
Programming: Python (NumPy, Pandas, SciPy), C++, R, MATLAB
ML/Statistics: Time series analysis, Factor models, Bayesian inference, NLP for finance
Finance: Options pricing, Portfolio optimization, Risk management (VaR, Greeks)
Infrastructure: Linux, SQL, kdb+/Q, Kafka
"""
    },
    {
        "name": "Nathan Wright",
        "file": "nathan_wright.txt",
        "content": """NATHAN WRIGHT
nathan.wright@email.com | (404) 555-1414 | Atlanta, GA

SUMMARY
Software Engineering Manager with 10+ years total experience (6 years engineering, 4 years management).
Led teams of 8-15 engineers delivering B2B SaaS products. Strong in agile delivery and team development.

EXPERIENCE

Engineering Manager | Salesforce | 2021 – Present
- Manage 3 teams (15 engineers) across CRM analytics product line ($50M ARR)
- Reduced time-to-production from 3 weeks to 4 days through process improvements
- Grew team from 8 to 15 through successful hiring and retention (0% attrition)
- Partnered with product and design to define multi-year technical roadmap

Senior Engineering Manager | NCR | 2019 – 2021
- Led platform engineering team (8 engineers) building POS software for retail
- Drove adoption of agile practices across 5 engineering teams
- Delivered $3M cost savings through technical debt reduction initiative

Software Engineer | NCR | 2013 – 2019
- Senior engineer → Tech lead → Manager progression
- Built transaction processing systems in Java and Python

EDUCATION
B.S. Computer Science | Georgia Tech | 2013

SKILLS
Leadership: Team building, Performance management, Roadmapping, Agile/Scrum, OKRs
Technical: Java, Python, AWS, microservices, system design
Tools: JIRA, Confluence, GitHub, DataDog, PagerDuty
"""
    },
    {
        "name": "Olivia Davis",
        "file": "olivia_davis.txt",
        "content": """OLIVIA DAVIS
olivia.davis@email.com | (617) 555-1515 | Cambridge, MA

SUMMARY
Biomedical Data Scientist with PhD in Computational Biology. 
Expert in genomics, bioinformatics, and ML applications in drug discovery.
Published 12 peer-reviewed papers in Nature, Cell, and PLOS Computational Biology.

EXPERIENCE

Senior Computational Scientist | Broad Institute | 2021 – Present
- Developed deep learning model for predicting CRISPR off-target effects (Nature Biotechnology)
- Built single-cell RNA sequencing analysis pipeline processing 1M+ cells
- Applied transformer models to protein structure prediction (AlphaFold fine-tuning)
- Collaborated with 8 wet-lab teams on data analysis

Postdoctoral Researcher | Harvard Medical School | 2019 – 2021
- Researched computational methods for rare disease variant interpretation
- Analyzed whole-genome sequencing data from 50,000+ patients

EDUCATION
Ph.D. Computational Biology | MIT | 2019
B.S. Biology & Computer Science | Johns Hopkins | 2014

SKILLS
Bioinformatics: GATK, STAR, DESeq2, Seurat, Scanpy, BioConductor
Languages: Python, R, Bash, Perl
ML: PyTorch, scikit-learn, deep learning, graph neural networks
Genomics: WGS/WES, scRNA-seq, ATAC-seq, ChIP-seq, metagenomics
Cloud: AWS, Google Cloud Life Sciences
"""
    },
    {
        "name": "Peter Zhang",
        "file": "peter_zhang.txt",
        "content": """PETER ZHANG
peter.zhang@email.com | (415) 555-1616 | San Francisco, CA

SUMMARY
Blockchain/Web3 Engineer with 5 years experience building DeFi protocols and smart contracts.
Deployed smart contracts handling $500M+ in TVL. Expert in Solidity, Rust, and DeFi architecture.

EXPERIENCE

Lead Smart Contract Engineer | Compound Finance | 2022 – Present
- Architected Compound III lending protocol (Solidity) managing $1B+ in assets
- Conducted security audits and implemented formal verification using Certora
- Built governance systems for on-chain voting with 50,000+ token holders
- Led 3-engineer team; managed $5M bug bounty program

Blockchain Engineer | Consensys | 2019 – 2022
- Developed DeFi primitives: AMMs, yield farming, staking contracts
- Built cross-chain bridges (Ethereum ↔ Polygon ↔ Arbitrum)
- Created developer tooling and SDKs for Ethereum ecosystem

EDUCATION
B.S. Computer Science | UC Berkeley | 2019

SKILLS
Smart Contracts: Solidity (expert), Vyper, Rust (Solana/Anchor)
Web3: Ethereum, Layer 2 (Arbitrum, Optimism, zkSync), Solana
Tools: Hardhat, Foundry, Truffle, OpenZeppelin, TheGraph
Frontend: TypeScript, ethers.js, wagmi, Next.js
Security: Formal verification, Audit tools (Slither, Mythril), CTF
"""
    },
    {
        "name": "Quinn Anderson",
        "file": "quinn_anderson.txt",
        "content": """QUINN ANDERSON
quinn.anderson@email.com | (503) 555-1717 | Portland, OR

SUMMARY
Technical Writer and Documentation Engineer with 7 years experience creating developer documentation 
for APIs, SDKs, and enterprise software. Strong technical background with coding experience.

EXPERIENCE

Senior Technical Writer | Twilio | 2021 – Present
- Own documentation for Twilio's Communication APIs (10M+ developer users)
- Reduced developer onboarding time by 45% through improved quickstart guides
- Built docs-as-code pipeline using Sphinx, GitHub Actions, and ReadTheDocs
- Collaborated with 20+ PMs and engineers to document new features at launch

Technical Writer | Atlassian | 2018 – 2021
- Wrote and maintained Confluence, JIRA, and Bitbucket documentation
- Created tutorial video scripts and interactive API playground content
- Developed internal style guide adopted across documentation team

EDUCATION
B.A. English/Linguistics | Reed College | 2017
Minor: Computer Science

SKILLS
Writing: API docs, User guides, Tutorials, Release notes, Style guides
Technical: REST/GraphQL APIs, Markdown, reStructuredText, OpenAPI/Swagger
Tools: Sphinx, Docusaurus, MadCap Flare, Confluence, GitHub
Programming: Python, JavaScript (basic), SQL (basic)
"""
    },
    {
        "name": "Rachel Kim",
        "file": "rachel_kim.txt",
        "content": """RACHEL KIM
rachel.kim@email.com | (213) 555-1818 | Los Angeles, CA

SUMMARY
Growth Marketing Manager with 6 years experience in data-driven marketing at consumer tech companies.
Expert in performance marketing, SEO/SEM, and marketing analytics. Managed $20M+ ad budgets.

EXPERIENCE

Senior Growth Manager | TikTok | 2021 – Present
- Managed $15M/quarter paid acquisition budget across Meta, Google, TikTok Ads
- Built attribution modeling reducing blended CAC by 28% ($4M savings)
- Launched influencer marketing program generating 500M+ organic views
- Led team of 4 growth marketers; reported directly to VP Marketing

Growth Marketing Manager | Spotify | 2018 – 2021
- Drove 25% YoY growth in premium subscriber conversions through A/B testing
- Optimized email lifecycle campaigns (automated flows, 4M+ subscribers)
- Built marketing analytics dashboards in Looker (SQL + Python)

Digital Marketing Analyst | WPP | 2017 – 2018
- Managed SEM campaigns for retail clients ($2M+ monthly spend)

EDUCATION
B.S. Marketing & Statistics | University of Michigan | 2017

SKILLS
Paid: Meta Ads, Google Ads, TikTok Ads, Programmatic, Apple Search Ads
Analytics: Google Analytics 4, Amplitude, Mixpanel, Looker, SQL, Python (basic)
Email: Braze, Iterable, Klaviyo, Mailchimp
SEO/Content: Ahrefs, SEMrush, content strategy, technical SEO
"""
    },
    {
        "name": "Samuel Thompson",
        "file": "samuel_thompson.txt",
        "content": """SAMUEL THOMPSON
samuel.thompson@email.com | (202) 555-1919 | Washington, DC

SUMMARY
Software Engineer with 3 years experience specializing in Python backend development and REST API design.
Recent graduate passionate about clean code, test-driven development, and open-source contributions.

EXPERIENCE

Software Engineer | Palantir Technologies | 2022 – Present
- Built data pipeline APIs for government analytics platform (Python, FastAPI)
- Developed ETL jobs processing classified datasets (clearance required)
- Wrote comprehensive unit and integration tests (95% code coverage)
- Participated in on-call rotation; resolved 50+ production incidents

Software Engineering Intern | Capital One | Summer 2021
- Built internal tool for credit risk analysis using Python and React
- Contributed features to microservices deployed on AWS Lambda

EDUCATION
B.S. Computer Science | University of Maryland | 2022
GPA: 3.9 | Honors thesis: "Efficient Graph Algorithms for Social Network Analysis"

SKILLS
Languages: Python (expert), JavaScript, Java, SQL
Frameworks: FastAPI, Flask, Django, React
Databases: PostgreSQL, DynamoDB, Redis
Cloud: AWS (Lambda, S3, RDS), Docker
Testing: pytest, unittest, Postman
"""
    },
    {
        "name": "Tina Patel",
        "file": "tina_patel.txt",
        "content": """TINA PATEL
tina.patel@email.com | (408) 555-2020 | Sunnyvale, CA

SUMMARY
NLP Engineer with 5 years specializing in conversational AI and language models.
Built production chatbots and NLP systems serving millions of users. 
Expert in Hugging Face, LangChain, and LLM fine-tuning.

EXPERIENCE

Senior NLP Engineer | Apple | 2021 – Present
- Led development of Siri intent classification system (BERT-based, 95% accuracy)
- Fine-tuned LLMs for domain-specific Q&A reducing hallucination by 60%
- Built RAG (Retrieval-Augmented Generation) pipeline for Siri Knowledge
- Optimized transformer models for on-device inference (Core ML conversion)

NLP Engineer | Nuance Communications | 2018 – 2021
- Built healthcare voice AI transcription system (98.5% accuracy)
- Developed named entity recognition for medical records (BioBERT)
- Created text classification pipeline for clinical notes routing

EDUCATION
M.S. Computational Linguistics | Stanford University | 2018
B.S. Computer Science & Linguistics | UCSD | 2016

SKILLS
NLP: Hugging Face Transformers, LangChain, SpaCy, NLTK, Gensim
Models: BERT, GPT-4, LLaMA, T5, Whisper, embedding models
Tasks: Text classification, NER, QA, Summarization, RAG, fine-tuning
MLOps: MLflow, Weights & Biases, ONNX, TensorRT
Languages: Python, SQL, Bash
"""
    },
    {
        "name": "Umar Hassan",
        "file": "umar_hassan.txt",
        "content": """UMAR HASSAN
umar.hassan@email.com | (347) 555-2121 | New York, NY

SUMMARY
Financial Analyst and FP&A professional with 6 years at investment banks and tech companies.
CFA charterholder. Expert in financial modeling, valuation, and business intelligence.

EXPERIENCE

Senior Financial Analyst | Meta | 2021 – Present
- Built integrated financial model for $30B advertising business unit
- Led quarterly earnings analysis for investor relations team
- Automated financial reporting saving 20 hours/week using Python and SQL
- Provided financial insights to VPs on headcount planning ($800M budget)

Financial Analyst | Morgan Stanley | 2018 – 2021
- Performed DCF, LBO, and comparable company analyses for M&A transactions
- Created pitch books for $2B+ technology sector deals
- Monitored portfolio companies and prepared investor reports

Analyst | Deloitte Consulting | 2017 – 2018
- Supported financial due diligence for private equity clients

EDUCATION
B.S. Finance & Economics | NYU Stern | 2017

SKILLS
Financial Modeling: DCF, LBO, M&A, three-statement modeling
Tools: Excel (VBA), Python (pandas), SQL, Tableau, Power BI, Bloomberg Terminal
Accounting: GAAP, IFRS, financial statement analysis
CERTIFICATIONS: CFA Charterholder | Series 63
"""
    },
    {
        "name": "Victoria Reyes",
        "file": "victoria_reyes.txt",
        "content": """VICTORIA REYES
victoria.reyes@email.com | (512) 555-2222 | Austin, TX

SUMMARY
Frontend Engineer with 4 years experience building performant React applications.
Passionate about accessibility, design systems, and web performance.
Open-source contributor with 5k+ GitHub stars.

EXPERIENCE

Frontend Engineer | Figma | 2022 – Present
- Contributed to core editor canvas performance (reduced re-renders by 60%)
- Built accessible component library used by 10+ product teams
- Implemented WebAssembly modules for CPU-intensive rendering operations
- Led frontend guild's web performance working group

Frontend Engineer | Shopify | 2020 – 2022
- Built merchant analytics dashboard (React + TypeScript + GraphQL)
- Improved Core Web Vitals scores: LCP -40%, CLS -80%, FID -50%
- Migrated legacy jQuery codebase to React (200k+ lines)

EDUCATION
B.S. Computer Science | UT Austin | 2020

SKILLS
Languages: TypeScript, JavaScript, HTML, CSS
Frameworks: React, Next.js, Remix, Vue.js, Svelte
Tools: Webpack, Vite, Storybook, Playwright, Cypress
Styling: Tailwind CSS, CSS Modules, styled-components, CSS-in-JS
Performance: Lighthouse, Web Vitals, Chrome DevTools, WebAssembly
Accessibility: WCAG 2.1, ARIA, screen reader testing
"""
    },
    {
        "name": "William Chen",
        "file": "william_chen.txt",
        "content": """WILLIAM CHEN
william.chen@email.com | (650) 555-2323 | Palo Alto, CA

SUMMARY
Site Reliability Engineer with 9 years of experience ensuring reliability and performance of distributed systems.
Expert in incident management, capacity planning, and observability. Led SRE teams at Google and Meta.

EXPERIENCE

Staff SRE | Meta | 2020 – Present
- Owned reliability for Instagram's feed ranking systems (2B+ daily users)
- Led incident management practice; achieved 99.999% availability SLA
- Built comprehensive observability platform (custom metrics, tracing, logging)
- Reduced on-call burden by 40% through intelligent alerting and runbook automation

Senior SRE | Google | 2015 – 2020
- Supported Google Search serving 8.5B+ daily queries
- Designed capacity planning models predicting 18-month infrastructure needs
- Developed chaos engineering toolkit used across 50+ Google SRE teams

EDUCATION
M.S. Computer Science | University of Illinois at Urbana-Champaign | 2015
B.S. Computer Engineering | Purdue University | 2013

SKILLS
Reliability: SLA/SLO/SLI design, Error budgets, Chaos engineering, Runbooks
Observability: Prometheus, Grafana, Jaeger, OpenTelemetry, ELK, Datadog
Cloud: GCP (expert), AWS, on-premise Linux
Programming: Go, Python, C++, SQL, Bash
On-call: PagerDuty, incident command, post-mortems
"""
    },
    {
        "name": "Xavier Johnson",
        "file": "xavier_johnson.txt",
        "content": """XAVIER JOHNSON
xavier.johnson@email.com | (773) 555-2424 | Chicago, IL

SUMMARY
Entry-level Data Analyst with 1 year of professional experience and strong academic background.
Passionate about turning data into actionable business insights using SQL, Python, and Tableau.

EXPERIENCE

Data Analyst | United Airlines | 2023 – Present
- Analyzes flight operations data to identify delay patterns (SQL, Python)
- Builds Tableau dashboards for operations team (20+ stakeholders)
- Automated weekly reporting, saving 8 hours/week

Data Analysis Intern | Nielsen | Summer 2022
- Supported media ratings analysis for broadcast TV clients
- Cleaned and processed datasets of 500k+ records using Python

EDUCATION
B.S. Statistics | DePaul University | 2023
GPA: 3.7 | Relevant coursework: Machine Learning, Time Series Analysis, Database Systems

SKILLS
Languages: SQL (advanced), Python (pandas, matplotlib, seaborn), R (basic)
BI Tools: Tableau, Power BI, Excel (advanced)
Databases: PostgreSQL, MySQL, Snowflake (basic)
Stats: Regression, Hypothesis testing, A/B testing
"""
    },
    {
        "name": "Yuki Tanaka",
        "file": "yuki_tanaka.txt",
        "content": """YUKI TANAKA
yuki.tanaka@email.com | (415) 555-2525 | San Francisco, CA

SUMMARY
Robotics Software Engineer with 5 years experience in autonomous systems and computer vision.
Expert in ROS/ROS2, C++, and perception systems for autonomous vehicles and drones.

EXPERIENCE

Robotics Engineer | Waymo | 2021 – Present
- Developed perception pipeline for autonomous vehicle sensor fusion (LiDAR + Camera)
- Built 3D object detection models achieving state-of-the-art on nuScenes benchmark
- Optimized real-time inference pipeline (C++ + CUDA) achieving 10x speedup
- Led sub-team of 4 engineers on pedestrian behavior prediction

Robotics Engineer | Boston Dynamics | 2019 – 2021
- Programmed locomotion control for Spot robot (ROS, C++)
- Developed manipulation algorithms for Pick robot in warehouse automation
- Built simulation environments in Gazebo for algorithm testing

EDUCATION
M.S. Robotics | Carnegie Mellon University | 2019
B.S. Mechanical Engineering | UC San Diego | 2017

SKILLS
Robotics: ROS/ROS2, Gazebo, MoveIt, Nav2, PCL
Computer Vision: OpenCV, PyTorch, 3D object detection, SLAM, sensor fusion
Languages: C++, Python, CUDA, Matlab
Hardware: LiDAR (Velodyne, Ouster), Cameras (Intel RealSense), IMU, GPS
"""
    },
    {
        "name": "Zoe Williams",
        "file": "zoe_williams.txt",
        "content": """ZOE WILLIAMS
zoe.williams@email.com | (646) 555-2626 | Brooklyn, NY

SUMMARY
Staff Software Engineer with 11 years of experience in distributed systems and platform engineering.
Passionate about developer productivity, system design, and engineering culture.

EXPERIENCE

Staff Engineer | Spotify | 2019 – Present
- Technical lead for internal developer platform used by 3,000+ engineers
- Designed event streaming architecture (Kafka) handling 1T+ events/day for music recommendations
- Contributed to engineering RFC process improving cross-team alignment
- Mentored 8 engineers to senior level; led system design interview panel

Senior Engineer | Twitter | 2014 – 2019
- Core contributor to Tweet ingestion pipeline (5,000 tweets/second)
- Led rewrite of notification delivery system reducing latency by 70%
- Drove adoption of service mesh (Linkerd) across 200+ microservices

EDUCATION
B.S. Computer Science | Cornell University | 2013

SKILLS
Languages: Scala, Java, Python, Go, SQL
Distributed Systems: Kafka, Flink, Spark, ZooKeeper, etcd
Databases: PostgreSQL, Cassandra, Redis, ClickHouse
Cloud: AWS, GCP, Kubernetes, Docker
System Design: Microservices, Event-driven, CQRS, saga patterns
"""
    },
    {
        "name": "Aaron Mitchell",
        "file": "aaron_mitchell.txt",
        "content": """AARON MITCHELL
aaron.mitchell@email.com | (214) 555-2727 | Dallas, TX

SUMMARY
Cloud Security Architect with 8 years experience securing cloud-native applications and infrastructure.
Expert in AWS security, identity management, and compliance automation. AWS CISO Advisory Board member.

EXPERIENCE

Principal Security Architect | AT&T | 2020 – Present
- Designed security architecture for telecom cloud transformation ($2B initiative)
- Built automated compliance platform (SOC 2, ISO 27001, NIST) reducing audit time 80%
- Led implementation of zero-trust network architecture for 300,000+ employees
- Managed security architecture team of 6 engineers

Senior Security Engineer | Palo Alto Networks | 2016 – 2020
- Developed cloud security posture management (CSPM) capabilities
- Researched and weaponized cloud attack patterns for red team operations
- Published 3 CVEs; presented at DEF CON and Black Hat

EDUCATION
B.S. Information Technology | Texas A&M University | 2016

SKILLS
Cloud Security: AWS Security Hub, GuardDuty, Azure Defender, GCP SCC
Identity: IAM, OAuth 2.0, SAML, PAM, Zero Trust
Compliance: SOC 2, ISO 27001, FedRAMP, PCI-DSS, HIPAA
Programming: Python, Terraform, Bash
CERTIFICATIONS: CISSP | AWS Security | GCP Security | CCSP
"""
    },
    {
        "name": "Brenda Foster",
        "file": "brenda_foster.txt",
        "content": """BRENDA FOSTER
brenda.foster@email.com | (612) 555-2828 | Minneapolis, MN

SUMMARY
Machine Learning Engineer with 4 years experience deploying ML models to production.
Expert in MLOps, model serving, and real-time ML systems. Strong Python and cloud skills.

EXPERIENCE

ML Engineer | Target Corporation | 2021 – Present
- Built recommendation system serving 2M+ daily users (matrix factorization + deep learning)
- Deployed 15+ ML models to production using Kubernetes and Seldon Core
- Built feature platform processing 50M+ events/day with Feast feature store
- Reduced model training time by 70% through distributed training on AWS SageMaker

ML Engineer | 3M | 2020 – 2021
- Deployed computer vision model for manufacturing quality control (98% defect detection)
- Built ML pipeline on Azure ML for materials science research team

EDUCATION
M.S. Computer Science | University of Minnesota | 2020
B.S. Software Engineering | Purdue University | 2018

SKILLS
ML/DL: PyTorch, TensorFlow, scikit-learn, XGBoost, Hugging Face
MLOps: MLflow, Kubeflow, Seldon, BentoML, Feast, Airflow
Cloud: AWS SageMaker, Azure ML, GCP Vertex AI
Languages: Python, SQL, Bash
Infra: Kubernetes, Docker, Spark, Kafka
"""
    },
    {
        "name": "Carlos Mendez",
        "file": "carlos_mendez.txt",
        "content": """CARLOS MENDEZ
carlos.mendez@email.com | (786) 555-2929 | Miami, FL

SUMMARY
iOS Developer with 6 years building mobile applications for healthcare and fintech.
Expert in Swift, SwiftUI, and HIPAA-compliant mobile development. App Store top-10 developer.

EXPERIENCE

Lead iOS Developer | Teladoc Health | 2021 – Present
- Built telehealth platform iOS app (Swift, SwiftUI) with 5M+ downloads
- Implemented end-to-end encrypted video consultations (WebRTC)
- Developed HIPAA-compliant data storage and transmission layer
- Reduced app crashes by 85% through systematic crash reporting analysis

iOS Developer | Chime | 2018 – 2021
- Built core banking features (account management, payments, P2P transfers) for 12M users
- Implemented biometric authentication (Face ID, Touch ID) with Keychain security
- Contributed to design system (60+ reusable Swift components)

EDUCATION
B.S. Computer Science | Florida International University | 2018

SKILLS
iOS: Swift (expert), SwiftUI, UIKit, Combine, Core Data, HealthKit
Security: Keychain, certificate pinning, HIPAA, PCI-DSS for mobile
Networking: REST, GraphQL, WebRTC, URLSession
Testing: XCTest, Quick/Nimble, UI Testing, TestFlight
Tools: Xcode, Instruments, Firebase, Fastlane, GitHub Actions
"""
    },
    {
        "name": "Diana Cho",
        "file": "diana_cho.txt",
        "content": """DIANA CHO
diana.cho@email.com | (425) 555-3030 | Bellevue, WA

SUMMARY
Principal Software Engineer with 12 years of experience in distributed systems and cloud infrastructure.
Led engineering teams building hyperscale cloud services at Microsoft and Amazon.
Frequent speaker at KubeCon and QCon; author of O'Reilly book on distributed systems.

EXPERIENCE

Principal Engineer | Amazon | 2018 – Present
- Technical lead for DynamoDB auto-scaling service serving 100M+ tables
- Designed consensus protocol improvement reducing P99 latency by 15%
- Led 6-person engineering team; drove 3 major feature launches
- Authored 12 Amazon internal design documents adopted as best practices

Senior Software Engineer | Microsoft | 2011 – 2018
- Core contributor to Azure Cosmos DB globally distributed database
- Designed multi-master replication protocol handling network partitions
- Presented at 5 industry conferences on consistency models

EDUCATION
Ph.D. Distributed Systems | MIT | 2011
B.S. Computer Science | Cornell University | 2006

SKILLS
Distributed Systems: Consensus algorithms (Paxos, Raft), CAP theorem, CRDT
Languages: Java, C++, Go, Python, SQL
Databases: DynamoDB, Cosmos DB, Cassandra, Spanner
Cloud: AWS (expert), Azure (expert)
"""
    },
    {
        "name": "Ethan Ross",
        "file": "ethan_ross.txt",
        "content": """ETHAN ROSS
ethan.ross@email.com | (704) 555-3131 | Charlotte, NC

SUMMARY
Junior Full-Stack Developer with 2 years experience and strong skills in React and Node.js.
CS bootcamp graduate turned professional. Quick learner; built 3 side projects in production.

EXPERIENCE

Software Developer | Bank of America | 2022 – Present
- Developed internal risk reporting tool (React + Node.js + PostgreSQL)
- Fixed 150+ bugs in legacy Java banking applications
- Contributed to agile team; completed sprint tasks consistently ahead of schedule

Software Developer Intern | LendingTree | Summer 2022
- Built loan comparison feature prototype using React
- Wrote SQL queries for financial analytics reports

EDUCATION
B.S. Computer Science | UNC Charlotte | 2022
GPA: 3.5

SKILLS
Frontend: React, JavaScript, HTML, CSS, Bootstrap
Backend: Node.js, Express, Python (basic), Java (basic)
Databases: PostgreSQL, MySQL, MongoDB (basic)
Tools: Git, GitHub, Docker (basic), JIRA, Postman
Testing: Jest, React Testing Library
"""
    },
    {
        "name": "Fiona Murphy",
        "file": "fiona_murphy.txt",
        "content": """FIONA MURPHY
fiona.murphy@email.com | (857) 555-3232 | Boston, MA

SUMMARY
Data Platform Engineer with 7 years building modern data infrastructure for analytics teams.
Expert in dbt, Snowflake, and data modeling. Transitioned from data analyst to engineering.

EXPERIENCE

Senior Analytics Engineer | DraftKings | 2021 – Present
- Owns core dbt project (500+ models) generating $180M sports betting analytics
- Built real-time odds analytics pipeline using Snowflake Dynamic Tables and Kafka
- Designed semantic layer enabling self-service analytics for 150+ business users
- Mentored team of 3 junior analytics engineers

Analytics Engineer | Wayfair | 2018 – 2021
- Migrated from Redshift to Snowflake, reducing query costs by 50%
- Built furniture recommendation data models powering A/B testing
- Created standardized data quality testing framework (dbt tests + Great Expectations)

Data Analyst | Liberty Mutual | 2016 – 2018
- Analyzed insurance claims data using SQL and Python
- Built Tableau dashboards for actuarial team

EDUCATION
B.S. Mathematics | Boston College | 2016

SKILLS
Data Modeling: dbt (expert), dimensional modeling, Kimball methodology
Warehouses: Snowflake, BigQuery, Redshift, Databricks
Languages: SQL (expert), Python, dbt Jinja/Macros
Orchestration: Airflow, Prefect, dbt Cloud
Visualization: Tableau, Looker, Metabase, Mode
"""
    },
    {
        "name": "George Walker",
        "file": "george_walker.txt",
        "content": """GEORGE WALKER
george.walker@email.com | (415) 555-3333 | San Francisco, CA

SUMMARY
AI/ML Product Engineer with 6 years bridging ML research and production systems.
Expert in LLM applications, prompt engineering, and AI product development.
Built AI products used by 5M+ users at leading tech companies.

EXPERIENCE

AI Engineer | Anthropic | 2023 – Present
- Built Claude API integrations and developer tooling for enterprise customers
- Designed evaluation frameworks for LLM safety and capability assessment
- Developed retrieval-augmented generation (RAG) systems for document Q&A
- Contributed to Constitutional AI implementation research

AI Engineer | Salesforce Einstein | 2020 – 2023
- Built GPT-powered CRM automation features (auto-summarization, email drafting)
- Developed multi-modal AI pipeline for document processing (OCR + NLP)
- Led integration of OpenAI API into Salesforce platform serving 150,000+ companies

Software Engineer | Zendesk | 2018 – 2020
- Built customer support automation using NLP (ticket classification, routing)
- Developed Python microservices for real-time NLP inference

EDUCATION
M.S. Artificial Intelligence | UC San Diego | 2018
B.S. Computer Science | UCLA | 2016

SKILLS
AI/ML: LLMs (GPT-4, Claude, LLaMA), RAG, prompt engineering, LangChain, LlamaIndex
NLP: Hugging Face, embeddings, vector databases (Pinecone, Chroma, Weaviate)
Languages: Python, TypeScript, SQL
Cloud: AWS, Azure OpenAI Service, GCP Vertex AI
"""
    },
]

def generate_resumes(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for resume in RESUMES:
        filepath = os.path.join(output_dir, resume["file"])
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resume["content"])
    print(f"Generated {len(RESUMES)} resumes in {output_dir}/")
    return len(RESUMES)

if __name__ == "__main__":
    count = generate_resumes("resumes")
    print(f"Total resumes: {count}")
