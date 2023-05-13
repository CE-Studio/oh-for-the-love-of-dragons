extends PopupMenu


# Called when the node enters the scene tree for the first time.
func _ready():
    visible = false
    for i in NodeManager.nodeNames:
        add_item(i)


func _on_id_pressed(id):
    var h:GraphNode = NodeManager.nodes[id].instantiate()
    var p = $"../VBoxContainer/GraphEdit".scroll_offset
    $"../VBoxContainer/GraphEdit".add_child(h)
    $"../VBoxContainer/GraphEdit".reposition(h)
