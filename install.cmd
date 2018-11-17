pyinstaller -F --noconsole ^
--add-data VERSION;. ^
--add-binary audio.pyd;. ^
--add-binary board.pyd;. ^
--add-binary card.pyd;. ^
--add-binary checker.pyd;. ^
--add-binary constants.pyd;. ^
--add-binary game.pyd;. ^
--add-binary loader.pyd;. ^
--add-binary player.pyd;. ^
--add-binary processes.pyd;. ^
--add-binary speech.pyd;. ^
--add-binary Tolk.pyd;. ^
--add-binary zones.pyd;. ^
--hidden-import pygame ^
--hidden-import xml.etree.ElementTree ^
--hidden-import cairosvg ^
main.pyw
