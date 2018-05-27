#encoding "utf-8"
#GRAMMAR_ROOT S
fio -> Word<gram="famn"> Word<gram="persn"> Word<gram="patrn">;
S -> fio interp (Names.Name);