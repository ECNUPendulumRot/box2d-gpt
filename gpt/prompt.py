from langchain.prompts.prompt import PromptTemplate
# from roscribe.parser import get_node_parser, get_topic_parser

def get_polygon_prompt():
    template = """
    AI正在使用Box2D物理引擎创建一个物体，需要使用Box2D中的Polygon，Edge和Circle设计一个Body。

AI最终输出一个json格式的图形属性字典, 其中包含构成一个Body的一些列fixture。
一个物体的json格式如下:  
```json
{{        
    "fixtures": [{{           
    	"shape-type": "polygon",             	
    	"vertices": [[0, 0], [1, 0], [1, 1], [0, 1]]      
    }}]     
}}
```

对于polygon类型的fixture，json格式如下：
```json
{{           
    "shape-type": "polygon",             	
    "vertices": [[0, 0], [1, 0], [1, 1], [0, 1]]      
}}
```
其中，vertices是顶点坐标列表, 坐标点只能是整数或浮点数, 不能是字符串. 

对于circle类型的fixture，json格式如下：
```json
{{
	"shape-type": "circle",
	"radius": 1,
	"position":[0, 0]
}}
```

AI应当且必须一次只问询一个问题。
AI将持续询问问题, 直到AI认为不需要进一步确认物体模板的细节为止。
AI不应该接连询问同一个问题。

在设计物体时，需要更好的视觉效果。

复杂的物体应当使用多个Fixture拟合。

AI需要仔细校验生成的json格式的正确性，确保在最终json中没有任何注释。

    AI应该只输出json字符串并以'END_OF_POLYGON_SPEC'结尾来结束对话, 不应该输出任何其他的说明性内容, 请确保除了'END_OF_POLYGON_SPEC'剩下的部分一定能被解析成json.

    当前对话:
    {history}
    Human: {input}
    AI:
    
    """
    return PromptTemplate(template=template, input_variables=["history", "input"]), "END_OF_POLYGON_SPEC"
