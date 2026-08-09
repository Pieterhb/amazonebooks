"""
Generate a fully static index.html with all book cards pre-rendered.
No JavaScript required to show images - they're directly in the HTML.
"""

import re, os

PANTHER = 'https://panther-ebooks.com'
SOFTCOVER = 'https://www.softcoverbooks.co.za'

panther_books = [
  {'title':'The Creeping Death','img':'/images/covers/10760_1774940080.jpg','store':'English','url':f'{PANTHER}/book-details/MTA3NjA%3D'},
  {'title':'Comrades of the Dragon','img':'/images/covers/10759_1774939568.jpg','store':'English','url':f'{PANTHER}/book-details/MTA3NTk%3D'},
  {'title':'The Blood Message','img':'/images/covers/10758_1774938905.jpg','store':'English','url':f'{PANTHER}/book-details/MTA3NTg%3D'},
  {'title':'La Sorciere Du Sahara','img':'/images/covers/10736_1771921502.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/MTA3MzY%3D'},
  {'title':'The Gallows in the Jungle','img':'/images/covers/10650_1761550849.jpg','store':'English','url':f'{PANTHER}/book-details/MTA2NTA%3D'},
  {'title':'Die Galg in die Oerwoud','img':'/images/covers/10649_1761549228.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/MTA2NDk%3D'},
  {'title':'The Maneaters of Tsavo','img':'/images/covers/10615_1757683870.jpg','store':'English','url':f'{PANTHER}/book-details/MTA2MTU%3D'},
  {'title':'Germ of Death','img':'/images/covers/10602_1755616334.jpg','store':'English','url':f'{PANTHER}/book-details/MTA2MDI%3D'},
  {'title':'The Baron of the Namib','img':'/images/covers/10601_1755613505.jpg','store':'English','url':f'{PANTHER}/book-details/MTA2MDE%3D'},
  {'title':'Death Creeps Closer','img':'/images/covers/10600_1755518622.jpg','store':'English','url':f'{PANTHER}/book-details/MTA2MDA%3D'},
  {'title':'Secret in the Grave','img':'/images/covers/10599_1755518186.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTk%3D'},
  {'title':'Murder in the Mine','img':'/images/covers/10598_1755517771.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTg%3D'},
  {'title':'Execute the Sentence','img':'/images/covers/10597_1755517407.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTc%3D'},
  {'title':'Death has Wings','img':'/images/covers/10596_1755517030.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTY%3D'},
  {'title':'The Deadly Triangle','img':'/images/covers/10595_1755516480.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTU%3D'},
  {'title':'Bloody the Darkness','img':'/images/covers/10594_1755516049.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTQ%3D'},
  {'title':'Fear Tonight','img':'/images/covers/10593_1755515668.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTM%3D'},
  {'title':'Victim of the Tokkelos','img':'/images/covers/10592_1755515010.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTI%3D'},
  {'title':'Stalkers in the Namib','img':'/images/covers/10591_1755514444.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTE%3D'},
  {'title':'The Snakes of Tumara','img':'/images/covers/10590_1755512873.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1OTA%3D'},
  {'title':'The Deranged Visitor','img':'/images/covers/10589_1755512239.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODk%3D'},
  {'title':'Spirit of the Witch Doctor','img':'/images/covers/10588_1755511730.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODg%3D'},
  {'title':'Vengeance from the Past','img':'/images/covers/10587_1755511058.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODc%3D'},
  {'title':'The Treasures of Monomotapa','img':'/images/covers/10586_1755510638.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODY%3D'},
  {'title':'Secret of the Cederberg','img':'/images/covers/10585_1755510066.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODU%3D'},
  {'title':'The Bloodhounds Bark','img':'/images/covers/10584_1755508826.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODQ%3D'},
  {'title':'Vultures of the Kalahari','img':'/images/covers/10583_1755508463.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODM%3D'},
  {'title':'Night of no Mercy','img':'/images/covers/10582_1755508077.jpg','store':'English','url':f'{PANTHER}/book-details/MTA1ODI%3D'},
  {'title':'Murder on Board Ship','img':'/images/covers/10469_1749561796.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0Njk%3D'},
  {'title':'Bonds of Death','img':'/images/covers/10468_1749561252.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0Njg%3D'},
  {'title':'Unrest in Namibia','img':'/images/covers/10467_1749560747.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0Njc%3D'},
  {'title':'The Fateful Date','img':'/images/covers/10466_1749560289.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NjY%3D'},
  {'title':'The Winged Fortune','img':'/images/covers/10465_1749559807.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NjU%3D'},
  {'title':'The Missing Girl','img':'/images/covers/10464_1749559346.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NjQ%3D'},
  {'title':'The Golden Dragon','img':'/images/covers/10463_1749558064.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NjM%3D'},
  {'title':'Scream at Night','img':'/images/covers/10449_1748708904.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDk%3D'},
  {'title':'Temple of Violence','img':'/images/covers/10447_1748707783.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDc%3D'},
  {'title':'Sweet Revenge','img':'/images/covers/10446_1748707067.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDY%3D'},
  {'title':'Darke Vengeance','img':'/images/covers/10445_1748705609.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDU%3D'},
  {'title':'The Deserters','img':'/images/covers/10444_1748705176.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDQ%3D'},
  {'title':'Area Zero','img':'/images/covers/10443_1748704624.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDM%3D'},
  {'title':'Bloody Ruby','img':'/images/covers/10442_1748706293.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDI%3D'},
  {'title':'Companions of Death','img':'/images/covers/10441_1748703846.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDE%3D'},
  {'title':'Vengeance Sweeps the Sahara','img':'/images/covers/10440_1748701909.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0NDA%3D'},
  {'title':'Shadows over the Sahara','img':'/images/covers/10439_1748699333.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0Mzk%3D'},
  {'title':'Bloodhound in the Sahara','img':'/images/covers/10438_1748698597.jpg','store':'English','url':f'{PANTHER}/book-details/MTA0Mzg%3D'},
  {'title':'Black Sails on the Horizon','img':'/images/covers/10292_1745661700.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyOTI%3D'},
  {'title':'In Enemy Hands','img':'/images/covers/10291_1745661299.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyOTE%3D'},
  {'title':'The Yellow Dragon','img':'/images/covers/10290_1745660922.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyOTA%3D'},
  {'title':'Stronghold of the Pirates','img':'/images/covers/10289_1745660197.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODk%3D'},
  {'title':'The Secret Mantle','img':'/images/covers/10288_1745659752.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODg%3D'},
  {'title':'The Skull','img':'/images/covers/10287_1745658567.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODc%3D'},
  {'title':'Predators from the East','img':'/images/covers/10286_1745658200.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODY%3D'},
  {'title':'The Coast of Barbary','img':'/images/covers/10285_1745657418.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODU%3D'},
  {'title':'Ghost Ship of Biscay','img':'/images/covers/10284_1745656062.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODQ%3D'},
  {'title':'The Blue Ruby','img':'/images/covers/10283_1745655530.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODM%3D'},
  {'title':"The Pirate's Treasure",'img':'/images/covers/10282_1745654986.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODI%3D'},
  {'title':'Arm from the Deep','img':'/images/covers/10281_1745654623.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODE%3D'},
  {'title':'The Black Seagull','img':'/images/covers/10280_1745653940.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyODA%3D'},
  {'title':'Sea Vultures','img':'/images/covers/10279_1745653605.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNzk%3D'},
  {'title':'The Spy','img':'/images/covers/10278_1745650097.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNzg%3D'},
  {'title':"Falcon in the Crow's Nest",'img':'/images/covers/10277_1745649621.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNzc%3D'},
  {'title':'The Ransom','img':'/images/covers/10276_1745649011.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNzY%3D'},
  {'title':'Captain Oloff the Pirate','img':'/images/covers/10271_1745587924.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNzE%3D'},
  {'title':'Scum of the Seas','img':'/images/covers/10270_1745587508.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNzA%3D'},
  {'title':'Sea of Vengeance','img':'/images/covers/10269_1745586939.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNjk%3D'},
  {'title':'Master of the Sword','img':'/images/covers/10268_1745586532.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNjg%3D'},
  {'title':'Deathtrap in the Desert','img':'/images/covers/10247_1770382820.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNDc%3D'},
  {'title':'Death in the Shadows','img':'/images/covers/10246_1770382703.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNDY%3D'},
  {'title':'Flames in the Temple','img':'/images/covers/10245_1770380253.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNDU%3D'},
  {'title':'Vengeance is Mine','img':'/images/covers/10244_1770380179.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNDQ%3D'},
  {'title':'Guests of Death','img':'/images/covers/10243_1770380086.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNDM%3D'},
  {'title':'Bloody Sunrise','img':'/images/covers/10241_1770379921.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyNDE%3D'},
  {'title':'Bloodstained Dunes','img':'/images/covers/10239_1770379747.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/MTAyMzk%3D'},
  {'title':'Curse of the Ruby','img':'/images/covers/10238_1770379617.jpg','store':'English','url':f'{PANTHER}/book-details/MTAyMzg%3D'},
  {'title':'Whispers of the Sunken Ship','img':'/images/covers/10011_1738592310.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMTE%3D'},
  {'title':'Pirates Execute the Verdict','img':'/images/covers/10010_1738591729.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMTA%3D'},
  {'title':'Curse of the Mad Pirate','img':'/images/covers/10009_1738591372.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMDk%3D'},
  {'title':"The King's Ransom",'img':'/images/covers/10008_1738590931.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMDg%3D'},
  {'title':'Quest for the Pearl of Malsia','img':'/images/covers/10007_1738590397.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMDc%3D'},
  {'title':'Echoes from the Sky','img':'/images/covers/10006_1738589965.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMDY%3D'},
  {'title':'Emerald of the High Seas','img':'/images/covers/10005_1738589533.jpg','store':'English','url':f'{PANTHER}/book-details/MTAwMDU%3D'},
  {'title':'Tamar and the Invaders','img':'/images/covers/9831_1735144732.jpg','store':'English','url':f'{PANTHER}/book-details/OTgzMQ%3D%3D'},
  {'title':'Tamar of the Forest','img':'/images/covers/9830_1735144605.jpg','store':'English','url':f'{PANTHER}/book-details/OTgzMA%3D%3D'},
  {'title':'Land of the Vampires','img':'/images/covers/9825_1734802417.jpg','store':'English','url':f'{PANTHER}/book-details/OTgyNQ%3D%3D'},
  {'title':'Revolution in the Jungle','img':'/images/covers/9824_1734802170.jpg','store':'English','url':f'{PANTHER}/book-details/OTgyNA%3D%3D'},
  {'title':'The Leopard Gang','img':'/images/covers/9823_1734801833.jpg','store':'English','url':f'{PANTHER}/book-details/OTgyMw%3D%3D'},
  {'title':'Hunters of Zarsjata','img':'/images/covers/9822_1734801443.jpg','store':'English','url':f'{PANTHER}/book-details/OTgyMg%3D%3D'},
  {'title':'The Octopus','img':'/images/covers/9821_1734800493.jpg','store':'English','url':f'{PANTHER}/book-details/OTgyMQ%3D%3D'},
  {'title':'Gold City of Sheba','img':'/images/covers/9820_1734800050.jpg','store':'English','url':f'{PANTHER}/book-details/OTgyMA%3D%3D'},
  {'title':'Riders of Death','img':'/images/covers/9815_1734612305.jpg','store':'English','url':f'{PANTHER}/book-details/OTgxNQ%3D%3D'},
  {'title':'Hoofbeats at Midnight','img':'/images/covers/9814_1734611627.jpg','store':'English','url':f'{PANTHER}/book-details/OTgxNA%3D%3D'},
  {'title':'No Forgiveness','img':'/images/covers/9813_1734611283.jpg','store':'English','url':f'{PANTHER}/book-details/OTgxMw%3D%3D'},
  {'title':'Beloved Traitor','img':'/images/covers/9812_1734610234.jpg','store':'English','url':f'{PANTHER}/book-details/OTgxMg%3D%3D'},
  {'title':'Traces in the Dew','img':'/images/covers/9811_1734609599.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/OTgxMQ%3D%3D'},
  {'title':'Judgement of the Mountains','img':'/images/covers/9810_1734608945.jpg','store':'English','url':f'{PANTHER}/book-details/OTgxMA%3D%3D'},
  {'title':'The Alley of Tears','img':'/images/covers/9809_1734608587.jpg','store':'English','url':f'{PANTHER}/book-details/OTgwOQ%3D%3D'},
  {'title':'Flame of the Lowveld','img':'/images/covers/9808_1734608050.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/OTgwOA%3D%3D'},
  {'title':'The Masked Robber Prevails','img':'/images/covers/9796_1755801383.jpg','store':'English','url':f'{PANTHER}/book-details/OTc5Ng%3D%3D'},
  {'title':'The Masked Robber Keeps Watch','img':'/images/covers/9795_1755801167.jpg','store':'English','url':f'{PANTHER}/book-details/OTc5NQ%3D%3D'},
  {'title':'Message for the Masked Robber','img':'/images/covers/9794_1755801010.jpg','store':'English','url':f'{PANTHER}/book-details/OTc5NA%3D%3D'},
  {'title':"The Masked Robber's Secret",'img':'/images/covers/9793_1755800936.jpg','store':'English','url':f'{PANTHER}/book-details/OTc5Mw%3D%3D'},
  {'title':'The Masked Robber Rides in the Night','img':'/images/covers/9792_1755800827.jpg','store':'English','url':f'{PANTHER}/book-details/OTc5Mg%3D%3D'},
  {'title':'The Red Ruby','img':'/images/covers/9776_1738587155.jpg','store':'English','url':f'{PANTHER}/book-details/OTc3Ng%3D%3D'},
  {'title':'Ravishing Armada','img':'/images/covers/9775_1745654253.jpg','store':'English','url':f'{PANTHER}/book-details/OTc3NQ%3D%3D'},
  {'title':'Deserter in Algeria','img':'/images/covers/9774_1733908557.jpg','store':'English','url':f'{PANTHER}/book-details/OTc3NA%3D%3D'},
  {'title':'Cavemen Valley','img':'/images/covers/9773_1734800967.jpg','store':'English','url':f'{PANTHER}/book-details/OTc3Mw%3D%3D'},
  {'title':'Masked Murderers','img':'/images/covers/9770_1757237521.jpg','store':'English','url':f'{PANTHER}/book-details/OTc3MA%3D%3D'},
  {'title':'The Masked Robber and his Gang','img':'/images/covers/8766_1755800579.jpg','store':'English','url':f'{PANTHER}/book-details/ODc2Ng%3D%3D'},
  {'title':'Long Live The Masked Robber','img':'/images/covers/8535_1755800464.jpg','store':'English','url':f'{PANTHER}/book-details/ODUzNQ%3D%3D'},
  {'title':'The Masked Robber','img':'/images/covers/8098_1755800345.jpg','store':'English','url':f'{PANTHER}/book-details/ODA5OA%3D%3D'},
  {'title':'The Fort is Quiet','img':'/images/covers/7744_1681219351.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/Nzc0NA%3D%3D'},
  {'title':'Revenge of the Desert','img':'/images/covers/7743_1681218940.jpg','store':'English','url':f'{PANTHER}/book-details/Nzc0Mw%3D%3D'},
  {'title':'The Scarlet Riders','img':'/images/covers/7742_1681218566.jpg','store':'English','url':f'{PANTHER}/book-details/Nzc0Mg%3D%3D'},
  {'title':'Footsteps to Death','img':'/images/covers/7741_1681217948.jpg','store':'English','url':f'{PANTHER}/book-details/Nzc0MQ%3D%3D'},
  {'title':'Witch of the Sahara','img':'/images/covers/7740_1681217481.jpg','store':'English','url':f'{PANTHER}/book-details/Nzc0MA%3D%3D'},
  {'title':'Revenge of the Sabre','img':'/images/covers/7726_1770379509.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/NzcyNg%3D%3D'},
  {'title':'Mademoiselle Julie','img':'/images/covers/7725_1770379435.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/NzcyNQ%3D%3D'},
  {'title':'The Tracks are Calling','img':'/images/covers/7724_1770379335.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/NzcyNA%3D%3D'},
  {'title':'Blood in front of the Sun','img':'/images/covers/7723_1770379226.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/NzcyMw%3D%3D'},
  {'title':'Thundering Hooves','img':'/images/covers/7722_1770379150.jpg','store':'Afrikaans','url':f'{PANTHER}/book-details/NzcyMg%3D%3D'},
]

softcover_books = [
  {'title':'Swart Luiperd — Die Swart Luiperd reeks (70 boeke)','img':'/images/covers/www.softcoverbooks.co.za_Swart%20Luiperd%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/swart luiperd reeks pronk.html'},
  {'title':'Sahara Avontuur reeks (40 boeke)','img':'/images/covers/www.softcoverbooks.co.za_Sahara%20logo.jpg','store':'Action','url':f'{SOFTCOVER}/sahara avontuur reeks pronk.html'},
  {'title':'Diamantveld Avontuur reeks','img':'/images/covers/www.softcoverbooks.co.za_Diamantveld%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/diamantveld reeks pronk.html'},
  {'title':'Swerwer Speurder reeks','img':'/images/covers/www.softcoverbooks.co.za_Swerwer%20Speurder%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/swerwer speurder reeks pronk.html'},
  {'title':'Rooi Jan reeks','img':'/images/covers/www.softcoverbooks.co.za_Rooi%20Jan%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/rooi jan reeks pronk.html'},
  {'title':'Temmers van die Woestyn reeks','img':'/images/covers/www.softcoverbooks.co.za_Temmers%20vd%20Woestyn%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/temmers van die woestyn reeks pronk.html'},
  {'title':'SA Polisie reeks','img':'/images/covers/www.softcoverbooks.co.za_SA%20Polisie%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/sa polisie reeks pronk.html'},
  {'title':'Oloff die Seerower — Pionier reeks','img':'/images/covers/www.softcoverbooks.co.za_Oloff%20Seerower%20Logo.jpg','store':'Action','url':f'{SOFTCOVER}/oloff die seerower pionier.html'},
  {'title':'Die Swart Luiperd — Fotoverhaal','img':'/images/covers/www.softcoverbooks.co.za_Swart%20Luiperd%20Logo.jpg','store':'Photo','url':f'{SOFTCOVER}/die swart luiperd reeks fotoverhaal.html'},
  {'title':'Grensvegter fotoverhale','img':'/images/covers/FOTOVERHALE_129.%20Grensvegter%20-%20Nes%20van%20onheil.jpg','store':'Photo','url':f'{SOFTCOVER}/grensvegter reeks fotoverhaal.html'},
  {'title':'Kid Colt fotoverhale','img':'/images/covers/FOTOVERHALE_137.%20Kid%20Colt%20-%20Bloody%20day%20at%20Comanche%20Creek.jpg','store':'Photo','url':f'{SOFTCOVER}/kid colt reeks fotoverhaal.html'},
  {'title':'Arend van die Oerwoud fotoverhale','img':'/images/covers/FOTOVERHALE_82.%20Arend%20Van%20Die%20Oerwoud%20-%20Verraad.jpg','store':'Photo','url':f'{SOFTCOVER}/arend van die oerwoud reeks fotoverhaal.html'},
  {'title':'Ruiter in Swart fotoverhale','img':'/images/covers/FOTOVERHALE_382.%20Ruiter%20in%20Swart%20-%20Kinders%20van%20onrus.jpg','store':'Photo','url':f'{SOFTCOVER}/ruiter in swart reeks fotoverhaal.html'},
  {'title':'Oerwoudvalk — Boeke Verkoop','img':'/images/covers/Images_1.%20Goudstad%20van%20Skeba.jpg','store':'Action','url':SOFTCOVER},
  {'title':'Maagd van die See reeks (9 boeke)','img':'/images/covers/www.softcoverbooks.co.za_Voorblad.jpg','store':'Action','url':f'{SOFTCOVER}/maagd van die see reeks pronk.html'},
  {'title':'Sahara Avontuur vrye eBoek','img':'/images/covers/www.softcoverbooks.co.za_freesaharaebook.jpg','store':'Action','url':SOFTCOVER},
  {'title':'Vrye Westerse eBoek','img':'/images/covers/www.softcoverbooks.co.za_freewesternebook.jpg','store':'Action','url':SOFTCOVER},
  {'title':'Voorblad Reeks 2','img':'/images/covers/www.softcoverbooks.co.za_Voorblad%202.jpg','store':'Photo','url':SOFTCOVER},
  {'title':'Voorblad Reeks 3','img':'/images/covers/www.softcoverbooks.co.za_Voorblad%203.jpg','store':'Photo','url':SOFTCOVER},
]

treasure_books = [
  {'title':'Skatkisboeke — Treasure Chest Collection','img':'/images/covers/www.softcoverbooks.co.za_Swart%20Luiperd%20Logo.jpg','store':'Story','url':SOFTCOVER},
  {'title':'Swart Luiperd — Sirkel/Vanity boeke','img':'/images/covers/www.softcoverbooks.co.za_Swart%20Luiperd%20Logo.jpg','store':'Story','url':f'{SOFTCOVER}/swart luiperd reeks sirkel.html'},
  {'title':'Sahara Avontuur — Sirkel boeke','img':'/images/covers/www.softcoverbooks.co.za_Sahara%20logo.jpg','store':'Story','url':f'{SOFTCOVER}/sahara avontuur reeks sirkel.html'},
  {'title':'Maagd van die See — Vanity boeke','img':'/images/covers/www.softcoverbooks.co.za_Voorblad.jpg','store':'Story','url':f'{SOFTCOVER}/maagd van die see reeks vanity.html'},
  {'title':'Ramala — Pionier boeke','img':'/images/covers/www.softcoverbooks.co.za_Diamantveld%20Logo.jpg','store':'Story','url':f'{SOFTCOVER}/ramala reeks pionier.html'},
  {'title':'Temmers van die Woestyn — Sirkel boeke','img':'/images/covers/www.softcoverbooks.co.za_Temmers%20vd%20Woestyn%20Logo.jpg','store':'Story','url':f'{SOFTCOVER}/temmers van die woestyn reeks sirkel.html'},
  {'title':'Oloff die Seerower — Sirkel boeke','img':'/images/covers/www.softcoverbooks.co.za_Oloff%20Seerower%20Logo.jpg','store':'Story','url':f'{SOFTCOVER}/oloff die seerower sirkel.html'},
  {'title':'Rooi Jan — Sirkel boeke','img':'/images/covers/www.softcoverbooks.co.za_Rooi%20Jan%20Logo.jpg','store':'Story','url':f'{SOFTCOVER}/rooi jan reeks sirkel.html'},
  {'title':'Die Gedoemde Dekaan — Fotoverhaal','img':'/images/covers/FOTOVERHALE_82.%20Arend%20Van%20Die%20Oerwoud%20-%20Verraad.jpg','store':'Photo','url':f'{SOFTCOVER}/die gedoemde dekaan reeks fotoverhaal.html'},
  {'title':'Arend van die Oerwoud — Fotoverhaal','img':'/images/covers/FOTOVERHALE_82.%20Arend%20Van%20Die%20Oerwoud%20-%20Verraad.jpg','store':'Photo','url':f'{SOFTCOVER}/arend van die oerwoud reeks fotoverhaal.html'},
  {'title':'Grensvegter fotoverhale','img':'/images/covers/FOTOVERHALE_129.%20Grensvegter%20-%20Nes%20van%20onheil.jpg','store':'Photo','url':f'{SOFTCOVER}/grensvegter reeks fotoverhaal.html'},
  {'title':'Oerwoudvalk Boeke','img':'/images/covers/Images_1.%20Goudstad%20van%20Skeba.jpg','store':'Story','url':SOFTCOVER},
]

def badge_class(store):
    m = {'Afrikaans':'badge-afrikaans','English':'badge-english','Action':'badge-softcover','Photo':'badge-treasure'}
    return m.get(store, 'badge-panther')

def card_html(book):
    title = book['title'].replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
    bc = badge_class(book['store'])
    return f'''    <article class="book-card" data-store="{book['store']}">
      <div class="book-img-wrapper">
        <img src="{book['img']}" alt="{title}">
        <span class="store-badge {bc}">{book['store']}</span>
      </div>
      <div class="book-content">
        <h3>{title}</h3>
        <p>Click below to view this book and discover more in the collection.</p>
        <a href="{book['url']}" target="_blank" rel="noopener" class="btn btn-primary">View Book</a>
      </div>
    </article>'''

def grid_html(books):
    return '\n'.join(card_html(b) for b in books)

home_featured = panther_books[:4] + softcover_books[:3] + treasure_books[:2]

css = open('style.css', encoding='utf-8').read()

nav_js = """
  // Navigation between sections
  document.querySelectorAll('[data-target]').forEach(function(el) {
    el.addEventListener('click', function(e) {
      e.preventDefault();
      var target = el.dataset.target;
      if (!target) return;
      document.querySelectorAll('.view').forEach(function(v) { v.classList.remove('active'); });
      var t = document.getElementById(target);
      if (t) t.classList.add('active');
      document.querySelectorAll('nav a').forEach(function(a) {
        a.classList.toggle('active', a.dataset.target === target);
      });
      window.scrollTo(0, 0);
    });
  });

  // Mobile menu toggle
  var menuBtn = document.getElementById('mobile-menu-btn');
  var navUl = document.querySelector('nav ul');
  if (menuBtn && navUl) {
    menuBtn.addEventListener('click', function() { navUl.classList.toggle('open'); });
    document.addEventListener('click', function(e) {
      if (!e.target.closest('nav') && !e.target.closest('#mobile-menu-btn')) navUl.classList.remove('open');
    });
  }

  // Filter buttons — show/hide cards by data-store
  document.querySelectorAll('.filter-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      var bar = btn.closest('.filter-bar');
      bar.querySelectorAll('.filter-btn').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      var store = btn.dataset.store;
      var gridId = bar.dataset.grid;
      document.querySelectorAll('#' + gridId + ' .book-card').forEach(function(card) {
        card.style.display = (store === 'all' || card.dataset.store === store) ? '' : 'none';
      });
    });
  });
"""

html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Discover 160+ unique Afrikaans &amp; English eBooks and classic Softcover series from Pieter Haasbroek. Panther eBooks, Treasure Chest Softcover Books — all in one place." />
    <meta name="keywords" content="ebook, afrikaans, english, pulp fiction, softcover, panther ebooks, treasure chest, swart luiperd, sahara, black panther series, buy ebook online" />
    <title>Pulp Fiction eBooks | Panther eBooks &amp; Softcover Classics</title>
    <style>
{css}
    </style>
  </head>
  <body>
    <header>
      <a href="#" class="logo" data-target="home">
        Pulp Fiction <span>eBooks</span>
      </a>
      <nav>
        <ul>
          <li><a data-target="home" class="active">Home</a></li>
          <li><a data-target="panther">Panther eBooks</a></li>
          <li><a data-target="softcover">Softcover Books</a></li>
          <li><a data-target="treasure">Treasure Chest</a></li>
        </ul>
      </nav>
      <button class="mobile-menu-btn" id="mobile-menu-btn" aria-label="Toggle menu">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6"/>
          <line x1="3" y1="12" x2="21" y2="12"/>
          <line x1="3" y1="18" x2="21" y2="18"/>
        </svg>
      </button>
    </header>

    <main>
      <!-- ===== HOME VIEW ===== -->
      <section id="home" class="view active">
        <div class="hero">
          <div class="hero-badge">🐆 Your One-Stop eBook Store</div>
          <h1>Discover Afrikaans &amp; English Classic Fiction</h1>
          <p>Explore 160+ thrilling eBooks and iconic Softcover series from Pieter Haasbroek. From the legendary Black Panther adventures to Sahara action stories — all available for download.</p>
          <div class="hero-btns">
            <a href="https://panther-ebooks.com/books" target="_blank" rel="noopener" class="btn btn-primary">
              🛒 Browse All eBooks
            </a>
            <a href="https://www.softcoverbooks.co.za" target="_blank" rel="noopener" class="btn btn-secondary">
              📖 Softcover Catalogue
            </a>
          </div>
        </div>

        <div class="stats-banner">
          <div class="stat-card"><span class="stat-number">160+</span><span class="stat-label">eBooks Available</span></div>
          <div class="stat-card"><span class="stat-number">70+</span><span class="stat-label">Swart Luiperd Titles</span></div>
          <div class="stat-card"><span class="stat-number">40+</span><span class="stat-label">Sahara Series Books</span></div>
          <div class="stat-card"><span class="stat-number">2</span><span class="stat-label">Languages: AF &amp; EN</span></div>
        </div>

        <div class="about-section">
          <div class="about-text">
            <h2>About Pieter Haasbroek</h2>
            <p>A retired scientist and passionate book collector, Pieter spent years digitising hundreds of classic Afrikaans and English pulp fiction books from a huge collection. Now he makes these thrilling eBooks available for everyone to download and enjoy.</p>
            <p>His collection spans action-adventure, detective stories, romance photo-novels, and more — preserving South Africa's rich literary heritage in digital form.</p>
            <a href="https://panther-ebooks.com/author" target="_blank" rel="noopener" class="btn btn-outline">Read Author Bio</a>
          </div>
          <div class="about-image">
            <div class="about-img-wrapper">
              <img src="/images/covers/10760_1774940080.jpg" alt="The Creeping Death - Panther eBook cover">
            </div>
          </div>
        </div>

        <h2 style="text-align:center; margin-top:3rem;">Latest eBooks</h2>
        <div class="product-grid" id="home-featured-grid">
{grid_html(home_featured)}
        </div>

        <div class="series-section">
          <h2>Featured Series</h2>
          <div class="series-grid">
            <div class="series-card" data-target="panther">
              <div class="series-icon">🐆</div>
              <h3>Panther eBooks</h3>
              <p>160+ Afrikaans &amp; English eBooks. PDF downloads available. The Black Panther, Sahara, and many more action series.</p>
              <span class="series-link nav-btn" data-target="panther">Explore →</span>
            </div>
            <div class="series-card" data-target="softcover">
              <div class="series-icon">📚</div>
              <h3>Softcover Books</h3>
              <p>Classic Afrikaans softcover story series including Swart Luiperd (70 books), Sahara Avontuur, SA Polisie, Oloff die Seerower, and many more.</p>
              <span class="series-link nav-btn" data-target="softcover">Explore →</span>
            </div>
            <div class="series-card" data-target="treasure">
              <div class="series-icon">💰</div>
              <h3>Treasure Chest</h3>
              <p>SKATKISBOEKE – Herinneringe van ou boeke is 'n skat om te geniet. Memories of old books is a treasure to enjoy.</p>
              <span class="series-link nav-btn" data-target="treasure">Explore →</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== PANTHER EBOOKS VIEW ===== -->
      <section id="panther" class="view">
        <div class="section-hero">
          <div class="section-hero-badge">🐆 Panther eBooks</div>
          <h2>Panther eBooks — Your One-Stop eBook Store!</h2>
          <p>If you are interested in superb online story eBooks as well as a wide variety of other types of eBooks, look no further. Satisfaction guaranteed. Available at <strong>panther-ebooks.com</strong></p>
          <a href="https://panther-ebooks.com/books" target="_blank" rel="noopener" class="btn btn-primary">Browse All Books on Panther eBooks</a>
        </div>
        <div class="filter-bar" data-grid="panther-grid">
          <button class="filter-btn active" data-store="all">All Books</button>
          <button class="filter-btn" data-store="Afrikaans">Afrikaans</button>
          <button class="filter-btn" data-store="English">English</button>
        </div>
        <div class="product-grid" id="panther-grid">
{grid_html(panther_books)}
        </div>
      </section>

      <!-- ===== SOFTCOVER BOOKS VIEW ===== -->
      <section id="softcover" class="view">
        <div class="section-hero">
          <div class="section-hero-badge">📚 Softcover Books</div>
          <h2>Africana Softcover Books — Classic Afrikaans Series</h2>
          <p>This site contains beautiful full-colour cover images of classic Afrikaans softcover story books and photo-novels from the 1950s–1980s. Now available as eBooks in PDF format at <strong>softcoverbooks.co.za</strong></p>
          <a href="https://www.softcoverbooks.co.za" target="_blank" rel="noopener" class="btn btn-primary">Visit Softcoverbooks.co.za</a>
        </div>
        <div class="filter-bar" data-grid="softcover-grid">
          <button class="filter-btn active" data-store="all">All Series</button>
          <button class="filter-btn" data-store="Action">Action &amp; Adventure</button>
          <button class="filter-btn" data-store="Photo">Photo Novels</button>
        </div>
        <div class="product-grid" id="softcover-grid">
{grid_html(softcover_books)}
        </div>
      </section>

      <!-- ===== TREASURE CHEST VIEW ===== -->
      <section id="treasure" class="view">
        <div class="section-hero">
          <div class="section-hero-badge">💰 Treasure Chest</div>
          <h2>SKATKISBOEKE — Treasure Chest Books</h2>
          <p><em>"Herinneringe van ou boeke is 'n skat om te geniet — Memories of old books is a treasure to enjoy."</em><br>Explore the full digital catalogue of Afrikaans classics available via the Treasure Chest Books website.</p>
          <a href="https://www.softcoverbooks.co.za" target="_blank" rel="noopener" class="btn btn-primary">Visit Treasure Chest Books</a>
        </div>
        <div class="filter-bar" data-grid="treasure-grid">
          <button class="filter-btn active" data-store="all">All Books</button>
          <button class="filter-btn" data-store="Story">Story Books</button>
          <button class="filter-btn" data-store="Photo">Photo Novels</button>
        </div>
        <div class="product-grid" id="treasure-grid">
{grid_html(treasure_books)}
        </div>
      </section>
    </main>

    <footer>
      <div class="footer-content">
        <div class="footer-brand">
          <p class="footer-logo">Pulp Fiction <span>eBooks</span></p>
          <p>Discover classic Afrikaans &amp; English fiction — eBooks and softcover series all in one place.</p>
          <p style="font-size:0.85rem; margin-top:0.5rem;">By Pieter Haasbroek · Retired scientist &amp; passionate book collector · South Africa</p>
        </div>
        <div class="footer-links-group">
          <h4>Our Stores</h4>
          <a href="https://panther-ebooks.com" target="_blank" rel="noopener">🐆 Panther eBooks</a>
          <a href="https://www.softcoverbooks.co.za" target="_blank" rel="noopener">📚 Softcoverbooks.co.za</a>
          <a href="https://panther-ebooks.com/track/order" target="_blank" rel="noopener">📦 Track Your Order</a>
        </div>
        <div class="footer-links-group">
          <h4>Collections</h4>
          <a href="#" class="nav-btn-footer" data-target="panther">Panther eBooks</a>
          <a href="#" class="nav-btn-footer" data-target="softcover">Softcover Books</a>
          <a href="#" class="nav-btn-footer" data-target="treasure">Treasure Chest</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Pieter Haasbroek · Pulp Fiction eBooks. All rights reserved. | <a href="https://panther-ebooks.com/terms" target="_blank" rel="noopener">Terms &amp; Conditions</a></p>
      </div>
    </footer>

    <script>
{nav_js}
    </script>
  </body>
</html>"""

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated dist/index.html ({len(html):,} bytes)")
print(f"  Panther books: {len(panther_books)}")
print(f"  Softcover books: {len(softcover_books)}")
print(f"  Treasure books: {len(treasure_books)}")
print(f"  Home featured: {len(home_featured)}")
