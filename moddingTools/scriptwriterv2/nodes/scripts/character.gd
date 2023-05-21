extends HBoxContainer


var charOnLeft := false:
    set(val):
        if val:
            $Button.disabled = true
            $Button2.disabled = false
        else:
            $Button2.disabled = true
            $Button.disabled = false
        charOnLeft = val


func _on_button1_pressed():
    $Button.disabled = true
    $Button2.disabled = false
    charOnLeft = true


func _on_button2_pressed():
    $Button2.disabled = true
    $Button.disabled = false
    charOnLeft = false
