SpendSense AI:
🧠 Smart Budget Tracker: Full-Stack Predictive Finance App
--


🧠 Project Overview
--
The Smart Budget Tracker is a modern, full-stack application designed to help users manage their personal finances through real-time expense tracking, bill splitting, and proactive, predictive budget analysis. It showcases a highly efficient and scalable architecture by separating the high-performance logic (FastAPI) from the interactive user interface (React).

The primary goal is to shift budget management from reactive tracking to predictive warning, using simple mathematical modeling as a proof-of-concept for deeper ML integration.

------------------
🎯 Project Objective
-

The primary objective of the Smart Budget Tracker project is threefold:

    Architectural Decoupling (Separation of Concerns): Successfully decouple the application's user interface (React) from its core business and predictive logic (FastAPI). This creates a scalable API layer capable of serving not just the current web application but also future mobile apps or reporting tools.


    

    Performance and Scalability: Leverage the high performance of the FastAPI framework and the analytical capabilities of Python to handle data validation and intensive calculations, ensuring the predictive analysis is fast, accurate, and ready to incorporate more complex Machine Learning (ML) models in the future.


    

    Data Persistence for ML: Integrate a persistent storage layer (SQLite) into the FastAPI backend to securely log all budget and expense data. This creates a valuable historical dataset, which is the foundational requirement for training and deploying advanced ML models (like time-series forecasting or anomaly detection) down the line.


    

In essence, the project transitions from a client-side calculator to a production-ready, API-driven platform centered around proactive financial prediction.

--------------
Here are the key features of the Smart Budget Tracker project, organized for clarity and highlighting the benefits of the full-stack architecture.

🔑 Key Features of the Smart Budget Tracker
------

Feature/USP	Description	Architectural Support
. Proactive Management (Prediction-Driven) 🎯

Theory: Effective budgeting requires shifting from reactive reporting to forward-looking prediction. The app uses a high-speed FastAPI backend to calculate spending velocity and project month-end status, delivering the 20th Date Alert as a critical, actionable warning that empowers the user to correct behavior immediately.

2. Social Accuracy (Integrated Expense Splitting) 🤝

Theory: Financial tracking must reflect real-world social complexities. By featuring seamless Split Expense Tracking, the app accurately isolates the user's true personal share of shared expenses. This ensures data integrity for individual budget analysis and prevents social costs from skewing predictive results.

3. Informed Optimization (Vlog/Blog Resources) 💡

Theory: Financial well-being is achieved through accessible, contextual learning. The app enhances the user experience by integrating Optimization Tips and Financial Vlog/Blog Resources. This provides just-in-time education tailored to expense categories, guiding users toward better habits and continuous spending optimization.

    ----------------
    🧰 Technologies Used
    --

The Smart Budget Tracker is built upon a high-performance, asynchronous full-stack foundation, ideal for integrating data-intensive logic.
<img width="1035" height="616" alt="image" src="https://github.com/user-attachments/assets/1819de82-b001-4881-8558-2026efe1348a" />



-----

📁 Project Structure
-
<img width="771" height="532" alt="image" src="https://github.com/user-attachments/assets/7551a2ce-8500-416e-a484-7bcfaf404641" />

--


⚙️ Installation & Setup Guide
--

Follow these steps to install and run the Smart Expense Management  application:-

Backend Terminal:
-
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

Frontend Terminal:
-
cd frontend
npm install
npm run dev

The application will be accessible in your browser (typically at http://localhost:5173 or http://localhost:3000).
-

Screenshots
--

<img width="1024" height="1024" alt="Gemini_Generated_Image_j05z7ej05z7ej05z" src="https://github.com/user-attachments/assets/b6c2e1d8-e9c5-4013-8a54-254eb5f70e37" />






<img width="1153" height="448" alt="image" src="https://github.com/user-attachments/assets/f674a7c6-ab6c-4c73-ac54-2c2a98413d41" />




<img width="1294" height="554" alt="Screenshot 2025-09-27 153602" src="https://github.com/user-attachments/assets/ee28be40-1fc3-43d9-a2a9-9610e8d30270" />








<img width="1302" height="569" alt="Screenshot 2025-09-27 153622" src="https://github.com/user-attachments/assets/00e9b747-c9c7-4419-8ac2-faa8582dcf3a" />











<img width="1297" height="568" alt="Screenshot 2025-09-27 153641" src="https://github.com/user-attachments/assets/d25e8b75-1e2d-4fc4-adb3-ca9d4185ed2e" />







Project vedio:-
--
https://drive.google.com/file/d/1gNJtec2x-_y7EMb-_7UGv4SY48PdB-MW/view?usp=sharing



