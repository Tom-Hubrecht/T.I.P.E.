let f x y = 
let p = ref (3 + x) in 
let cste = (3) in 
for i = 10 to 15 do
print_int(2 + i);
done;
print_int(!p);
print_string("Hello, world");
p := 15;
print_int(!p);
;;
