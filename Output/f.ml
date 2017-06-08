let f x y = 
let p = ref (3 + x) in 
let cste = 3 in 
for i = 10 to 15 do
print_int(2 + i);
print_newline();
done;
while !p != 9 do
p := !p + 1;
print_int(!p);
print_newline();
done;
if !p = 2 then
begin
print_int(!p);
print_newline();
end
else
begin
print_string("Toto");
print_newline();
end;
print_string("Hello, world");
print_newline();
p := 15;
print_int(!p);
print_newline();
;;
