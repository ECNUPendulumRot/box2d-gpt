from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory

from model import llm_init
from prompt import get_polygon_prompt


def main(verbose=False):
    llm = llm_init()

    init_human_input = input("Human: ")

    polygon_prompt, polygon_end_str = get_polygon_prompt()

    polygon_memory = ConversationBufferMemory()

    polygon_chain = ConversationChain(
        llm=llm,
        prompt=polygon_prompt,
        memory=polygon_memory,
        verbose=verbose)
    
    polygon_output = polygon_chain.predict(input=init_human_input)

    print("AI: " + polygon_output)

    while polygon_end_str not in polygon_output:
        human_response = input("Human: ")
        polygon_output = polygon_chain.predict(input=human_response)
        spec_output_clean = polygon_output.replace(polygon_end_str, "")
        print("AI: " + spec_output_clean)

    print("finish")
    


if __name__ == "__main__":
    main()
