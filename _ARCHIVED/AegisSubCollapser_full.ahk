;AegisSubCollapser
;Peter Adriano DeBiase
;2013/03/23
;updated 2015/11/14
;Collapses 4 subtitles into one subtitle in Aegissub

#SingleInstance force
CoordMode, Mouse, Screen ;sets mouse stuff to use screen coords

;HOTKEY (q + 1)
q & 1::


;Select the line you want to start at

Loop, 38
{
	; Send +{Down} ;Select next line
	; Sleep, 10
	; Send +{Down} ;Select next line
	; Sleep, 10
	; Send +{Down} ;Select next line
	; Sleep, 10
	; Send +{Down} ;Select next line
	; Sleep, 10
	; Send +{Down} ;Select next line
	; Sleep, 10
	; Send +{Down} ;Select next line
	; Sleep, 10
	Send +{Down 6} ;Select six lines
	; Sleep, 10

	Send {Alt}{Right 2}{Enter} ;Select Subtitle menu
	Sleep, 10
	
	Send {Down 11}{Enter} ;Select Join Lines
	Sleep, 10

	Send {Enter} ;Concatenate
	Sleep, 10
	
	Send {Down}
}

^1::Return ;If anything goes wrong for any reason, just press this key combo to quit the current thang