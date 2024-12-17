from langchain_core.prompts import PromptTemplate


class ReactPrompt:
    """
    A class to encapsulate the React Prompt Template for AI-Assistant interactions in Korean.
    """

    def __init__(self):
        """
        Initializes the ReactPromptTemplate with required parameters.

        :param tools: Description of the available tools.
        :param tool_names: Names of the available tools.
        :param input_question: The input question for the AI-Assistant.
        :param agent_scratchpad: The agent's intermediate scratchpad thoughts or reasoning.
        """
        self.react_prompt_template = """
        You are an AI-Assistant with access to tools for answering questions effectively. Respond in Korean. Available tools: {tools}

        To use a tool, follow this format:

        '''
        Thought: Need a tool? Yes
        Action: [one of {tool_names}]
        Action Input: [input for the tool]
        Observation: [tool result]
        ... (repeat up to 3 times)
        '''

        If no tool is needed, respond as follows:

        '''
        Thought: Need a tool? No
        Final Answer: [response in Korean]
        '''

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}
        """

        # Correctly initialize PromptTemplate with template and input_variables
        self.prompt = PromptTemplate(
            template=self.react_prompt_template,
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
        )

    def get_prompt(self) -> PromptTemplate:
        """
        Returns the PromptTemplate instance.

        :return: PromptTemplate object.
        """
        return self.prompt
