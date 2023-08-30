# Vision 
**A-Jarvis (AJ)** is an AI copilot for designing, deploying, and optimizing enterprise software architecture. The current practice of enterprise architecture design follows a fragmented process. An enterprise software architect, leveraging their years of expertise,  uses a business requirement to produce a solution architecture to deliver the desired business outcomes. This technical design is generally at the systems concept level, as defined by [Simon Brown](https://simonbrown.je/) in his **C4 Model** architecture. Software developers, who follow a more formal SDLC process that includes CI/CD, take this design and develop the represented solution shared by the architect. In the C4 model, the developers implement custom logic that connects multiple container apps composed of various components. Each component consists of code written by the developer. Hence the [C4](https://c4model.com/)= **Concepts, Container, Component, Code**. The vision of this project is to create a copilot that helps enterprise software developers and architects seamlessly work across all layers of the C4 model using natural language in a single workspace.

# Motivation

Historically, the life cycle of an enterprise solution architecture is long (often years) and experiences very few changes. Rapid ideation happens early in the process, captured in diagrams as concepts of the options considered. Once an enterprise architecture is designed, there is often no direct code synthesis from the diagrams. New business demands drive updates to the architecture. However, that process is mainly ad-hoc. UML was the most mature effort to address this need for formalism. However, it failed to have broad adoption, in part due to its complexity. We surmise that  enterprise software architecture design has suffered in the following ways:
<ol>
<li>A lack of formalism, as seen in other areas of computer science. This ad hoc approach has resulted in a soup of ad hoc approaches. </li>
<li> Static diagrams that, once generated, are decoupled from the deployment/runtime environment produced.</li>
<li>Diagrams are not code: Many diagramming tools produce binary and proprietary outputs. Diagrams cannot be quickly composed and inherited as done normatively with modern object-oriented programming broadly practiced in software engineering. Consequently, enterprise architecture cannot leverage git and other CI/CD tools for versioning and tracking.
</li>
<li>Non-validating Design:  The lack of feedback from the runtime environment to the design results in a blind architecture design. This lack of validation results in a draw-and-forget-it design mode of operation among architects. Diagrams are meant for communicating ideas and may have low fidelity. If an operator wants to know the truth of the system state, operators should look at other consoles or dashboards. These dashboards need not have any resemblance to source architecture. Consider the difference between a manufacturing plant and a chemical processing diagram. The high fidelity of these diagrams is such that operators can use them on the monitoring dashboard to show the plant state retrieved by sensors.   
</li>
<li>
AI Unfriendly. LLM AI works best when formalism exists, such as a design language with a  large sample set of qualified examples. Without such a corpus of data, any approach to leveraging AI/LLM to build a copilot requires hand-crafting this initial data set. 
</li>  
</ol>

# Fullstack: Diagram to Direct Code Synthesis 
Many subsystems (components and containers) now have regularized patterns that lend to their description in domain-specific languages (Yaml) or access by API calls in familiar development languages such as Python. As a result,  increasingly AI, such as Github copilot, can generate high-quality code when provided with prompts. Consequently, the development path from diagram to code is more amenable to direct synthesis than ever. AJ will allow architects and software engineers to collaborate in a unified development ecosystem to quickly validate key features of architecture (e.g., diagrams checked in as code).

# Goals
AJ aims to materially change the practice of enterprise software architecture by collapsing the distance between ideation and the rest of the SDLC. These are the  principal outcomes:
<ol>
<li>
Use natural language to describe system design and query system properties. 
</li>
<li>
Diagrams as code via DSL that have the composable properties of modern object-oriented programming language.
</li>
<li>
Generate a suite of prompts to train an LLM to generate DSL for set sample architectures. 
Direct synthesis ( or generation) of code and other deployment assets from diagrams. (e.g., generate Bicep or Kubeflow)
</li>
<li>
Self-validating by the capture of observability signals from the deployed system and representing system state in the architecture diagram
</li>
<li>
Enable rapid experimentation through a Jypter-like interface. 
</li>
</ol>

# Resources
We will use [Structurizr](https://structurizr.com/)  "diagrams as code (dac)" DSL to design our training set of reference architectures. We aim to have the LLM model learn the DSL and then be able to generate valid Structurizr code in response to natural language prompts. 

# Milestones:
TBD

# Run from the root of the project.
```
$ pip install -e .
# Command to run the app.
$ uvicorn agents.main:app --host 0.0.0.0 --port 8000 --reload
```
Navigate to http://0.0.0.0:8000/docs, where you will see the Swagger UI with the endpoint to test. Submit your payload and check the output.

To create the AI agent paste the content in the file [first](prompts/first.json)
```
{
    "context": "You are a enterprise software architect specializing in diagrams written in the structurizr language with a maximum of 10 containers. The user can have many software architecture views or instances of model that provides different granularity of views, and your job is always to analyze and guide them to use the diagrams that gives the clearest view of the resiliency of the architecture. The response should include detailed information on the diagrams. The response should also include questions to the user when necessary. If you think your response may be inaccurate or vague, do not write it and answer with the exact text: `I don't have a response. `",
    "first_message": "Hello, I am AJ your personal enterprise architect designer and system analyst and I am here to help you with your architecture design and your analysis. What can I do for you today?",
    "response_shape": "{'diagrams': 'Structurizr diagram', 'views': 'List of the views used in the diagrams', 'summary': 'String, summary of the architecture function of the diagram'}",
    "instructions": "Run through the conversation messages and discard any messages that are not relevant for enterprise software architecture design and analysis. Focus on extracting the designs that were mentioned in the conversation and for each of them extract the list of diagrams. Make sure to provide a summary of the conversation when asked."
}
```

**The Deployment Cycle**

We will deploy our application under a container environment in the cloud such as Kubernetes, Azure Container Service, or AWS Elastic Container Service. Here is where we create a docker image and upload our code so we can run it in one of these environments, go ahead and open the Dockerfile one we created at the start and paste the following code:

```
# Dockerfile
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install the package using setup.py
RUN pip install -e .

# Install dependencies
RUN pip install pip -U && \
    pip install --no-cache-dir -r requirements.txt

# Set the environment variable
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose the necessary ports
EXPOSE 8000

# Run the application
# CMD ["uvicorn", "agents.main:app", "--host", "0.0.0.0", "--port", "8000"]

```


The Dockerfile installs the app and then it runs it via the CMD which is commented out. You should uncomment the command if you want to run it locally as a standalone, but for other services such as Kubernetes, this is defined when defining the deployment or pods in the command section of the manifest.

Build the image, wait until the build is completed, and then test it by running the run command, which is below:



# Build the image
```
$ docker build - build-arg OPENAI_API_KEY=<Replace with your OpenAI Key> -t agents-app .
```
Run the container with the command from the agents app (Use -d flag for the detached run).
```
$ docker run -p 8000:8000 agents-app uvicorn agents.main:app --host 0.0.0.0 --port 8000
```

# Output
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     172.17.0.1:41766 - "GET / HTTP/1.1" 200 OK
INFO:     172.17.0.1:41766 - "GET /favicon.ico HTTP/1.1" 404 Not Found
INFO:     172.17.0.1:41770 - "GET /docs HTTP/1.1" 200 OK
INFO:     172.17.0.1:41770 - "GET /openapi.json HTTP/1.1" 200 OK
```

# Run the front-end code
The code below connects to our agent's microservice via API calls and allows the user to select the Agent and the Conversations and chat with the agent, similar to what ChatGPT provides. Let’s run this app by opening another terminal (make sure you have the agents microservice up and running on port 8000) and type:

``` 
$ streamlit run src/frontend/main.py and you are ready to go!
```

<hl>
This is fork of conversational-ai 
It is described in the article below Conversational AI services - follow the article on medium: https://medium.com/@cfloressuazo/building-a-conversational-agent-with-memory-microservice-with-openai-and-fastapi-5d0102bc8df9.


