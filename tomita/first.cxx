#encoding "utf-8"
#GRAMMAR_ROOT S
init -> AnyWord<wff=/[А-Я]./>;
fio -> Word<gram="famn"> Word<gram="persn"> Word<gram="patrn">;
fiosh -> Word<gram="famn"> init init;
S -> fio interp (Names.Name::not_norm) | fiosh interp (Names.Name::not_norm);