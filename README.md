               # **🌌 KNOWLEDGE BASE AGENT**


## **📌 Project Overview**

**Category**: Business Operations (Knowledge Base Agent)

- The Knowledge Base Agent (codenamed Gemini Neural Hub) is a next-generation AI assistant designed to act as a secure, intelligent "Second Brain" for enterprise data. Unlike traditional keyword search tools, it utilizes Retrieval Augmented Generation (RAG) powered by Google's advanced Gemini 1.5/2.5 models to read, understand, and reason across entire PDF documents instantly.

- This project features a unique "Smart Model Switcher" engine that automatically routes queries to the optimal Google model (Flash, Pro, or Legacy) to ensure 100% uptime and zero 404 errors, wrapped in a stunning Cyberpunk/Sci-Fi interface.
- 

## **📸 Project Visuals**

**1. The Neural Interface (Dashboard)**

   ![Dashboard Interface](assets/dashboard_view.png)

- A futuristic HUD for document ingestion and real-time telemetry.

**2. Intelligent Reasoning (Chat)**

   ![Chat Interface](assets/chat_view.png)

- The agent answering complex queries with structural diagrams.
  

## **🚀 Key Features**

1) **🧠 Smart Brain Engine**

- Auto-Failover: Automatically detects API errors (404/429) and switches between gemini-1.5-flash, gemini-1.5-pro, and gemini-2.0 models instantly.

- Context-Aware: Injects full document context into the system prompt for high-fidelity answers.

2) **🎨 Cyberpunk HUD Interface**

- Immersive Design: Features animated particle backgrounds, glassmorphism panels, and neon typography.

- Interactive Feedback: Visual and simulated auditory cues (toast notifications) for system status.

3) **🖼️ Auto-Diagramming**

- Visual Thinking: Intelligently detects requests for "structures", "flows", or "processes" and automatically generates Graphviz/DOT diagrams to visualize the data.

4) **📊 Live Telemetry**

- Real-Time Stats: A sidebar dashboard showing page counts, character volume, and simulated network latency.

5) **🛡️ Enterprise Security**

- Ephemeral Processing: API Keys and Document data are processed in-memory and cleared upon session reset. Zero permanent storage.
  

## **🛠️ Tech Stack**

| Component          | Technology                             | Description                                 |
| ------------------ | -------------------------------------- | ------------------------------------------- |
| **Frontend**       | Streamlit                              | Custom Cyberpunk UI with CSS overrides      |
| **AI Core**        | Google Gemini API (Flash, Pro, Legacy) | RAG-style reasoning & diagram generation    |
| **Backend Logic**  | Python                                 | Smart model routing, error handling         |
| **PDF Processing** | `pypdf`                                | Fast text extraction                        |
| **Visualization**  | Graphviz                               | Auto-rendering workflows & process diagrams |
| **Memory Layer**   | In-Memory                              | Zero data retention for security            |



## **🏗️ Architecture**

![System Architecture](assets/architecture_diagram.png)

**1) Ingestion Layer:** User uploads a PDF. The Streamlit app uses pypdf to extract raw text and metadata.

**2) Context Injection:** The extracted text is optimized and injected into the System Prompt of the GeminiAgent.

**3) Smart Routing Layer:** The GeminiBrain attempts connection with the priority model (Flash). If a 404 or connection error occurs, it seamlessly fails over to Pro or Legacy models in real-time.

**4) Generation Layer:** The active Gemini model generates a markdown response. It decides whether to output text or graphviz code based on the query.

**5) Rendering Layer:** The Frontend renders the markdown text and compiles any DOT code into visible diagrams instantly.


## **⚙️ Setup & Run Instructions**

   - Follow these steps to deploy the agent locally:

**1) Clone the Repository:**

     git clone https://github.com/Syed-centem/ai-agent.git

     cd ai-agent


**2) Install Dependencies:**
  - Ensure you have Python installed, then run:

     pip install -r requirements.txt


**3) Run the Application:**

     streamlit run app.py


**4) Initialize the System:**

 -> Open the link provided in the terminal (usually http://localhost:8501).

 -> Enter your Google Gemini API Key in the secure sidebar HUD.

 -> Upload a PDF document.

 -> Click the "INITIATE NEURAL LINK" button.
 

## **🔮 Future Roadmap**

[ ] **Voice Integration:** Adding Speech-to-Text (STT) for hands-free queries.

[ ] M**ulti-Modal Analysis:** Ability to read charts and images inside PDFs.

[ ] **Persistent Memory:** Integration with ChromaDB for storing chat history across sessions.

