from database import SessionLocal, engine, Base
from models import Job

Base.metadata.create_all(bind=engine)

jobs = [
    Job(title="Backend Engineer", company="Google",
        location="Remote",
        description="Build scalable REST APIs using Python and cloud infrastructure. Experience with microservices and databases required.",
        skills="Python,FastAPI,PostgreSQL,Docker,AWS,REST API"),

    Job(title="Frontend Developer", company="Microsoft",
        location="Hyderabad",
        description="Build modern React applications with TypeScript. Work on large-scale web products used by millions.",
        skills="React,TypeScript,JavaScript,HTML,CSS,Git"),

    Job(title="Data Scientist", company="Amazon",
        location="Bangalore",
        description="Analyse large datasets, build ML models, and drive business decisions with data insights.",
        skills="Python,Pandas,NumPy,Scikit-learn,SQL,Machine Learning"),

    Job(title="ML Engineer", company="Flipkart",
        location="Bangalore",
        description="Train and deploy machine learning models at scale. Work with NLP and recommendation systems.",
        skills="Python,TensorFlow,PyTorch,NLP,MLOps,Docker"),

    Job(title="Full Stack Developer", company="Infosys",
        location="Pune",
        description="Develop end-to-end web applications. Work on both React frontend and Node.js backend.",
        skills="React,Node.js,JavaScript,MongoDB,Express,REST API"),
]

db = SessionLocal()
db.add_all(jobs)
db.commit()
db.close()
print("Jobs seeded successfully!")