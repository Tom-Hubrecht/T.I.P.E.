let f x y = 
let p = ref (3 + x) in 
let cste = 3 in 
for i = 10 to 15 do
print_int(2 + i);
done;
if !p = 2 then
begin
print_int(!p);
end
print_string("Hello, world");
p := 15;
print_int(!p);
;;
