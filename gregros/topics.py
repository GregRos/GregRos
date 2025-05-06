from typing import Iterable
from gregros.topic import Topic, Topics

cat_personal = Topic("personal")
cat_package = Topic("package") - Topic("incomplete") - Topic("obsolete")
cat_incomplete = Topic("incomplete") + cat_package
cat_obsolete = Topic("obsolete")
cat_sample = Topic("sample")

type_lib = Topic("library") + cat_package
type_fw = Topic("framework") + cat_package
type_tool = Topic("tool") - cat_obsolete
type_hotkeys = Topic("hotkeys")
lang_typescript = Topic("typescript") + cat_package
lang_python = Topic("python") + cat_package
lang_rust = Topic("rust")
lang_csharp = Topic("csharp", display="C#")
lang_fsharp = Topic("fsharp", display="F#")
lang_scala = Topic("scala")
lang_kotlin = Topic("kotlin")
lang_bash = Topic("bash")
lang_ahk = Topic("ahk", display="AutoHotKey")
tech_k8s = Topic("kubernetes", display="Kubernetes")
tech_vscode = Topic("vscode", display="VSCode")
tech_dotnet = Topic("dotnet", display=".NET")
tech_react = Topic("react")
tech_unicode = Topic("unicode")
tech_dom = Topic("dom", display="DOM")
dom_parsing = Topic("parsing") + cat_package
dom_modding = Topic("modding") + cat_package
dom_printing = Topic("print", display="Printing") + cat_package
dom_testing = Topic("testing", display="Testing") + cat_package
dom_scripting = Topic("scripting") + cat_package
dom_binding = Topic("binding")
dom_rpc = Topic("rpc", display="RPC")
para_functional = Topic("functional-programming", display="Functional")
para_reactive = Topic("reactive-programming", display="Reactive")
para_aspect = Topic("aspect-oriented-programming", display="Aspect-Oriented")

topic_locals = {
    name: topic
    for name, topic in locals().items()
    if isinstance(topic, (Topic, Topics))
}


def get_prefixed_with(prefix: str) -> dict[str, Topic | Topics]:
    return {
        name: Topics(topic)
        for name, topic in topic_locals.items()
        if isinstance(topic, (Topic, Topics)) and name.startswith(prefix)
    }


exported = {
    "tech": get_prefixed_with("tech_"),
    "lang": get_prefixed_with("lang_"),
    "type": get_prefixed_with("type_"),
    "cat": get_prefixed_with("cat_"),
    "dom": get_prefixed_with("dom_"),
    "para": get_prefixed_with("para_"),
}
