# Automator V 0.1

![cover image](#cover.png)

Automator V 0.1 is a Python-based project that uses OpenAI's GPT-3.5-turbo model to help decompose software development problems into smaller deliverables and generate code for the specified deliverables.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have a working Python 3.6+ environment.
* You have an OpenAI API key to access the GPT-3.5-turbo model.

## Installation

To set up the project, follow these steps:

1. Clone the repository.

```bash
git clone https://github.com/your-username/automator-v0.1.git
cd automator-v0.1
```

2. Install the required Python packages.

```bash
pip install -r requirements.txt
``` 


3. Create a `.TOKEN.txt` file in the root directory of the project and add your OpenAI API key.

```bash
echo "your-openai-api-key" > .TOKEN.txt

```


## Usage

Run the main script to start the application:

```bash
python main.py
```


Follow the prompts to describe your problem, and the application will classify the problem, decompose it into smaller deliverables, and generate code for each deliverable.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
