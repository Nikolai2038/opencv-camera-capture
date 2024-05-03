FROM debian:12.5

# Update system packages
RUN apt update && apt upgrade -y

# Project directory
WORKDIR /app

# ========================================
# Prepare Python
# ========================================
# Install Python
RUN apt update && apt install -y python3

# Install virtual environment
RUN apt update && apt install -y python3-venv
# Create virtual environment
RUN python3 -m venv venv
# Set virtual environment as global
ENV PATH="/app/venv/bin:${PATH}"

# Install "pip"
RUN apt update && apt install -y python3-pip

# Для избежания ошибки "ImportError: libGL.so.1: cannot open shared object file: No such file or directory" при работе с "cv2":
# Install "opencv" for "cv2" requirement
RUN apt update && apt install -y python3-opencv
# ========================================

# ========================================
# Install project
# ========================================
# # Install requirements
COPY ./requirements.txt ./requirements.txt
RUN --mount=type=cache,target=/root/.cache pip install -r ./requirements.txt

# Copy project files
COPY ./main.py ./main.py
COPY ./input ./input
# ========================================

CMD ./main.py
