extends GraphNode
class_name BaseGraphNode


var connectedTo = {}


# Called when the node enters the scene tree for the first time.
func _ready():
    var b := Button.new()
    get_titlebar_hbox().add_child(b)
    b.pressed.connect(_close)


func _close():
    var h:GraphEdit = get_parent()
    for i in h.get_connection_list():
        if i["to_node"] == name:
            h.disconnect_node(i["from_node"], i["from_port"], i["to_node"], i["to_port"])
            var j:BaseGraphNode = get_node("../" + i["from_node"])
            j.connectedTo.erase(i["to_node"])
        elif i["from_node"] == name:
            h.disconnect_node(i["from_node"], i["from_port"], i["to_node"], i["to_port"])
    queue_free()
