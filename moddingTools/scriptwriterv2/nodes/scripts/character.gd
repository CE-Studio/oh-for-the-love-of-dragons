extends HBoxContainer


var charOnLeft := false:
	set(val):
		print(val == charOnLeft)
		if val:
			$Button.disabled = true
			$Button2.disabled = false
		else:
			$Button.disabled = false
			$Button2.disabled = true
		$Button.set_pressed_no_signal(false)
		$Button2.set_pressed_no_signal(false)
		charOnLeft = val


func _on_button1_pressed():
	print("b1")
	$Button.disabled = true
	$Button2.disabled = false
	charOnLeft = true


func _on_button2_pressed():
	print("b2")
	$Button2.disabled = true
	$Button.disabled = false
	charOnLeft = false
