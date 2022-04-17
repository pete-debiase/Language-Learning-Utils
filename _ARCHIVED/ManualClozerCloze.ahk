;ManualClozerCloze
;Peter Adriano DeBiase
;2013/03/24
;For use with Subs2srs cards in Anki - replaces highlighted text with [...] and turns it bold and blue

;HOTKEY (q + 1)
q & 1::

;Select the text you want to cloze
Send [...]
Sleep, 2
Send +{Left}
Sleep, 2
Send +{Left}
Sleep, 2
Send +{Left}
Sleep, 2
Send +{Left}
Sleep, 2
Send +{Left}
Sleep, 2

Send ^b
Sleep, 2
Send {F7}
Sleep, 2
Send {F6}


