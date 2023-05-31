FROM arm64v8/python:3.10.11-buster AS build

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc build-essential libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install llama-cpp-python==0.1.50
# RUN pip install --no-cache-dir git+https://github.com/abetlen/llama-cpp-python.git
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# # second unnamed stage
# FROM arm64v8/python:3.9.16-slim-buster AS dependencies
# WORKDIR /

# COPY requirements.txt .
# # install dependencies to the local user directory (eg. /root/.local)
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --default-timeout=500 -r requirements.txt


FROM arm64v8/python:3.10.11-slim-buster
WORKDIR /

# COPY --from=build /usr/include/x86_64-linux-gnu/ /usr/include/x86_64-linux-gnu/
# COPY --from=build /usr/lib/x86_64-linux-gnu/ /usr/lib/x86_64-linux-gnu/

# copy only the dependencies installation from the 1st stage image
# Copy the installed pip packages from Stage 2
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# Copy the installed pip packages from Stage 2
# COPY --from=dependencies /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
# Install Streamlit

COPY . .

# Set the PATH environment variable
ENV PATH="/usr/local/bin:${PATH}"

EXPOSE 8501

# CMD ["streamlit", "run", "verse/window.py"]

CMD [ "python","-m", "verse" ]
# CMD [ "verse/window.py", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]