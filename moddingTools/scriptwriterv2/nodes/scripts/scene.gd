extends BaseGraphNode


@onready
var charlist:VBoxContainer = $VBoxContainer/HBoxContainer2/VBoxContainer
var charbase:PackedScene = preload("res://nodes/scripts/character.tscn")


func _on_char_add():
	charlist.add_child(charbase.instantiate())


func _on_char_remove():
	var h = charlist.get_child_count()
	if h > 0:
		charlist.get_child(h - 1).queue_free()
