extends PopupMenu


@onready var signals := {
	"Organize": $"../TabContainer/Graph/Graph".arrange_nodes
}


# Called when the node enters the scene tree for the first time.
func _ready():
	visible = false
	for i in NodeManager.nodeNames:
		add_item(i)
	add_separator()
	for i in signals.keys():
		add_item(i)


func _on_id_pressed(id):
	if id < NodeManager.nodes.size():
		var h:GraphNode = NodeManager.nodes[id].instantiate()
		$"../TabContainer/Graph/Graph".add_child(h)
		$"../TabContainer/Graph/Graph".reposition(h)
	else:
		signals[get_item_text(id)].call()
