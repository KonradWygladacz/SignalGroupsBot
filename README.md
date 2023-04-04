# SignalGroupsBot

- żeby bot wszedł w pozycje w wiadomości na telegramie muszą być uzyte słowa: leverage i entry
- Zawsze wchodzi za ~10$ na dzwigni x10, Isolated, One-Way mode
- Wchodzi w pozycje od razu po aktualnej cenie(nie czeka na entry zone)
- Targety ustawia w przyblizeniu. Wiec jesli liczba Qty jest niepodzielna przez liczbe targetów to nie wszystkie Qty zostaną wpisane w targety
- jak cos pojdzie nie tak(np. chatgpt źle rozpisze wartości lub wiadomosc nie bedzie zawierala stop lossa) to program ominie ten sygnał i poczeka na nastepny
