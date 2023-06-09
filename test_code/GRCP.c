// versinon w14
// 2023.05.23
#include "gc.h"

// ファイル読み込みと標準入力を分けて、(include filename)をできるようにした。
// string OK
// prim_eval && prim_apply OK
// Float
// operator + - * /
// quas-quote do now

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <assert.h>
//man lib_name
//top -u
//port boem gc for windlow
//chocoreate pakage search
union Object;

typedef union Object Object;
typedef Object *oop;
typedef oop (*prim_t)(oop,oop);

typedef enum { ILLEGAL, Undefined, Integer, Double, String, Symbol, Primitive, Special, Closure, Cell } type_t;

struct Integer  { type_t type; int   value; };
struct Double   { type_t type; double value;};
struct String   { type_t type; char *value; };
struct Symbol   { type_t type; char *name;  oop value;};
struct Primitive{ type_t type; oop name; prim_t function;};
struct Special  { type_t type; oop name; prim_t function;};
struct Closure  { type_t type; oop name; oop parameter, expression, environment;};
struct Cell     { type_t type; oop a, d;  };

union Object
{
    type_t type;
    struct Integer Integer;
    struct Double Double;
    struct String  String;
    struct Symbol  Symbol;
    struct Primitive Primitive;
    struct Special Special;
    struct Closure  Closure;
    struct Cell    Cell;
};

// global symbol
oop nil     = 0;
oop t       = 0;
oop globals = 0;
oop syntax  = 0;

// function 
oop sym_define = 0;
oop sym_syntax = 0;
oop sym_lambda = 0;
oop sym_quote  = 0;
oop sym_quasiquote = 0;
oop sym_unquote = 0;
oop sym_unquote_splicing = 0;

// + - * /
oop sym_plus  = 0;
oop sym_minus = 0;
oop sym_multi = 0;
oop sym_divid = 0;
oop sym_equal = 0;

// == < <= > >=
oop sym_less       = 0;

// if while for 
oop sym_if 	  = 0;
oop sym_while = 0;

// appendix GRCP-10
oop sym_print = 0;
oop sym_println = 0;
oop sym_let     = 0;
oop sym_setq    = 0;

oop sym_env_define = 0;
oop sym_eqn = 0;

oop newObject(type_t type)
{
    oop obj = calloc(1, sizeof(Object));
    obj->type = type;
    return obj;
}

type_t Object_type(oop obj)
{
    assert(obj); // not a NULL pointer
    return obj->type;
}

oop newInteger(int value)
{
    oop obj = newObject(Integer);
    obj->Integer.value = value;
    return obj;
}

oop newDouble(double value){
    oop obj = newObject(Double);
    obj->Double.value = value;
    return obj;
}

oop newString(char* value){
    oop obj = newObject(String);
    obj->String.value = value;
    return obj;
}

int Integer_value(oop obj)
{
    assert(Object_type(obj) == Integer);
    return obj->Integer.value;
}

double Double_value(oop obj){
    assert(Object_type(obj) == Double);
    return obj->Double.value;
}

char *Symbol_name(oop obj)
{
    assert(Object_type(obj) == Symbol);
    return obj->Symbol.name;
}

char *String_value(oop obj)
{
    assert(Object_type(obj) == String);
    return obj->String.value;
}

prim_t Primitive_func(oop obj){
    assert(Object_type(obj)==Primitive);
    return obj->Primitive.function;
}

prim_t Special_func(oop obj){
    assert(Object_type(obj)==Special);
    return obj->Special.function;
}

oop Closure_parameters(oop obj){
    assert(Object_type(obj)==Closure);
    return obj->Closure.parameter;
}

oop Closure_expressions(oop obj){
    assert(Object_type(obj)==Closure);
    return obj->Closure.expression;
}
oop Closure_environment(oop obj){
    assert(Object_type(obj)==Closure);
    return obj->Closure.environment;
}

int  symbolCount = 0;
oop *symbolTable = 0;

oop newSymbol(char *name)
{
    int lo = 0, hi = symbolCount - 1;
    while (lo <= hi) {
	int mi = (lo + hi) / 2;
	oop sym = symbolTable[mi];
	int cmp = strcmp(name, Symbol_name(sym));
	if      (cmp < 0) hi = mi - 1;
	else if (cmp > 0) lo = mi + 1;
	else              return sym;
    }
    oop obj = newObject(Symbol);
    obj->Symbol.name = strdup(name);
    obj->Symbol.value = nil;
    symbolTable = realloc(symbolTable, sizeof(oop) * (symbolCount + 1));
    for (int i = symbolCount;  i > lo;  --i)
	symbolTable[i] = symbolTable[i-1];
    ++symbolCount;
    symbolTable[lo] = obj;

    return obj;
}

oop newCell(oop a, oop d)
{
    oop obj = newObject(Cell);
    obj->Cell.a = a;
    obj->Cell.d = d;
    return obj;
}

oop newPrimitive(prim_t function)
{
    oop obj = newObject(Primitive);
    obj->Primitive.function = function;
    obj->Primitive.name = nil;
    return obj;
}

oop newSpecial(prim_t function)
{
    oop obj = newObject(Special);
    obj->Special.function = function;
    obj->Special.name = nil;
    return obj;
}

oop newClosure(oop parameters, oop expressions,oop environment){
    oop obj = newObject(Closure);
    obj->Closure.parameter   = parameters;
    obj->Closure.expression  = expressions;
    obj->Closure.environment = environment;
    obj->Closure.name = nil;
    return obj;
}

/*////////////////////////////////////////////////////////

    NORMAL FUNC
    
////////////////////////////////////////////////////////*/

oop Cell_a(oop obj)	{ assert(Object_type(obj) == Cell);  return obj->Cell.a; }
oop Cell_d(oop obj)	{ assert(Object_type(obj) == Cell);  return obj->Cell.d; }

void Cell_setA(oop obj, oop a)	{ assert(Object_type(obj) == Cell);  obj->Cell.a = a; }
void Cell_setD(oop obj, oop d)	{ assert(Object_type(obj) == Cell);  obj->Cell.d = d; }


int isident(int c)
{
    return isalpha(c) || strchr("!#$%&*+-/:;<=>?\\^_|~", c);
}

int nextchar(void)
{
    int c = getchar();
    while (isspace(c)||c==';'){
        if(c==';'){
            while(c!='\n'){
                c = getchar();
            }
        }
        else
        c = getchar();
    }
    return c;
}

oop revlist(oop list, oop tail)
{
    while (Object_type(list) == Cell) { // list not empty
	oop cell = list;      // the first cell in list
	list = list->Cell.d;  // remove cell from list
	cell->Cell.d = tail;  // push cell onto the
	tail = cell;          //   front of tail
    }
    return tail;
}

oop car(oop obj);       
oop cdr(oop obj);                                                                          // ! no
oop eval(oop exp,oop env);
oop cadr(oop obj);
oop assoc(oop obj,oop alist);
oop apply(oop,oop,oop);
void println(oop);

oop read(void) // read stdin and return an object, or 0 if EOF
{
    int c;
    c = nextchar();
    if (isdigit(c) || c=='.') { // asdf
        int length = 0;
        char buf[32];
        int isDot = 0;
        while(isdigit(c) && length<sizeof(buf)-1){
            buf[length++] = c;
            c = getchar();
        }
        if(c == '.'){
  
            do{
                buf[length++] = c;
                c = getchar();
            }while(isdigit(c) && length<sizeof(buf)-1);
            buf[length] = 0;
            if(length!=1)ungetc(c,stdin);
            if(length>1){
                return newDouble(atof(buf));
            }
        }
        buf[length] = 0;
        ungetc(c,stdin);
        if(length>0)
            return newInteger(atoi(buf));
        fprintf(stderr,"ERROR: not allow dot only\n");
        exit(1);
    }

    if (isident(c)) { // symbol
        char string[64];
        int length = 0;
        do {
            string[length++] = c;
            c = getchar();
        } while((isident(c) || isdigit(c)) && length < sizeof(string) - 1);
        ungetc(c, stdin);
        string[length] = '\0';
        if (!strcmp(string, "nil")) return nil;
        return newSymbol(string);
    }
    if (c == '\"'){
        char string[64];
        int length = 0;
        int c;
        while(length < sizeof(string) - 1 && ((c=getchar())!='\"')){
            string[length++] = c;
        }
        string[length] = '\0';
        return newString(strdup(string));
    }
    
    if(c=='`'){
        oop list = read();
        return newCell(sym_quasiquote,newCell(list,nil));
    }
    if(c==','){
        c = nextchar();
        if(c=='@'){
            oop list = read();
            return newCell(sym_unquote_splicing,newCell(list,nil));
        }
        ungetc(c,stdin);
        oop list = read();
        return newCell(sym_unquote,newCell(list,nil));
    }
// 'a -> (quote a)
    if (c == '\''){
        oop list = read();
        return newCell(sym_quote,newCell(list,nil));
    }
    if (c == '(') { // ( a b (a b))
        oop list = nil;
        c = nextchar();
        while (c != ')' && c != '.') {
            ungetc(c, stdin);
            oop obj = read();
            if (!obj) {
            fprintf(stderr, "EOF while reading list\n");
            exit(1);
            }
            list = newCell(obj, list); // push element onto front of list
            c = nextchar();
        }
        oop last = nil;
        if (c == '.') {
            last = read();
            if (!last) {
            fprintf(stderr, "EOF while reading list\n");
            exit(1);
            }
            c = nextchar();
        }
        if (c != ')') {
            fprintf(stderr, "')' expected at end of list\n");
            exit(1);
        }

        oop newlist = revlist(list,last);
        oop head = car(newlist);
        if(Object_type(head)==Symbol){
            oop ass = assoc(head,syntax);
            if(ass!=nil){
                oop value = cdr(ass);
                return apply(value,newlist,nil);
            }
        }
        return newlist;
    }
    if (c == EOF) return 0;
    fprintf(stderr, "illegal character: [%c] 0x%02x\n", c,c);
    exit(1);
    return 0;
}


void print(oop obj)
{
    switch (Object_type(obj)) {
	case ILLEGAL: {
	    fprintf(stderr, "ILLEGAL type encountered\n");
	    abort();
	}
	case Undefined: printf("nil"); return;
	case Integer:	printf("%d", Integer_value(obj));return;
    case Double:    printf("%f", Double_value(obj));return;
    case String:    printf("%s", String_value(obj));return;
	case Symbol:	printf("%s", Symbol_name(obj)) ;return;
    case Primitive: print(obj->Primitive.name);return;//printf("%p",Primitive_func(obj));return;
    case Special :  print(obj->Special.name);return;//printf("%p", Special_func(obj)); return;
    case Closure:{
        printf("<Closure.");
        print(obj->Closure.name);
        printf("> <exp.");
        print(Closure_expressions(obj));
        printf("> <para.");
        print(Closure_parameters(obj));
        printf("> <env.");
        print(Closure_environment(obj));
        putchar('>');
        return;
    }
	case Cell: { // (1 . (2 . (3 . nil))) -> (1 2 3)
	    putchar('(');
	    for (;;) {
		print(obj->Cell.a);
		obj = obj->Cell.d;
		if (Object_type(obj) != Cell) break;
		putchar(' ');
	    }
	    if (nil != obj) {
		printf(" . ");
		print(obj);
	    }
	    putchar(')');
	    return;
	}
    }
    assert(0); // this can never be reached
}

void println(oop obj)
{
    if(obj!=nil){
    print(obj);
    putchar('\n');
    }
}


oop car(oop obj){return (Object_type(obj)==Cell)?obj->Cell.a:nil;}
oop cdr(oop obj){return (Object_type(obj)==Cell)?obj->Cell.d:nil;}
oop cadr(oop obj){return car(cdr(obj));}
oop caddr(oop obj){return car(cdr(cdr(obj)));}
oop cddr(oop obj){return cdr(cdr(obj));}

oop assoc(oop obj,oop alist){
	while(Object_type(alist)==Cell){
		oop list = car(alist);
		if(car(list)==obj)
			return list;
		alist = cdr(alist);
	}
    return nil;
}

oop pairlist(oop names,oop values,oop tail){
    if(Object_type(names)!=Cell){
        return (names==nil)
            ?tail
            :newCell(newCell(names,values),tail);
    }
    oop name = names->Cell.a;
    oop value = car(values);
    return newCell(newCell(name,value),pairlist(names->Cell.d,cdr(values),tail));
}

oop evlist(oop list,oop env){
	if(Object_type(list)!=Cell){
		return eval(list,env);
	}
	return newCell(eval(list->Cell.a,env),evlist(list->Cell.d,env));
}

/*////////////////////////////////////////////////////////

    PRIM FUNCION
    
////////////////////////////////////////////////////////*/
oop define(oop name, oop value);
oop apply(oop func,oop args,oop env);

// PRIM FUNCTION

oop prim_less(oop args,oop env)
{
    oop arg = car(args);
    if(Object_type(arg)!=Integer){
        fprintf(stderr,"Integer arg [prim_less]");
        exit(1);
    }
    while(Object_type(cdr(args))==Cell){
        args = cdr(args);
        if(Integer_value(arg)>=Integer_value(car(args)))
            return nil;
        arg = car(args);
    }
    return t;
}

// (+ car(args) cadr(args))
oop prim_plus(oop args,oop env)
{
    int value = 0;
    for(;;){
        if(Object_type(args)!=Cell)return newInteger(value);
        if(Object_type(car(args))!=Integer)break;
        value += Integer_value(car(args));
        args = cdr(args);
    }
    double fvalue = value;
    for(;;){
        if(Object_type(args)!=Cell)return newDouble(fvalue);

        if(Object_type(car(args))==Integer)fvalue+=(double)Integer_value(car(args));
        else fvalue += Double_value(car(args));
        args = cdr(args);
    }
    fprintf(stderr,"ERROR:prim_plus\n");
    exit(1);
    return 0;
}

oop prim_minus(oop args,oop env)
{
    int value = 0;
    for(;;){
        if(Object_type(args)!=Cell)return newInteger(value);
        if(Object_type(car(args))!=Integer)break;
        value -= Integer_value(car(args));
        args = cdr(args);
    }
    double fvalue = value;
    for(;;){
        if(Object_type(args)!=Cell)return newDouble(fvalue);
        if(Object_type(car(args))!=Double)break;
        fvalue -= Double_value(car(args));
        args = cdr(args);
    }
    fprintf(stderr,"ERROR:prim_plus\n");
    exit(1);
    return 0;
}
                       
oop prim_multi(oop args,oop env)
{
    int value = 1;
    for(;;){
        if(Object_type(args)!=Cell)return newInteger(value);
        if(Object_type(car(args))!=Integer)break;
        value *= Integer_value(car(args));
        args = cdr(args);
    }
    double fvalue = value;
    for(;;){
        if(Object_type(args)!=Cell)return newDouble(fvalue);
        if(Object_type(car(args)))break;
        fvalue *= Double_value(car(args));
        args = cdr(args);
    }
    fprintf(stderr,"ERROR:prim_plus\n");
    exit(1);
    return 0;
}

oop prim_divid(oop args,oop env)
{
    int value = 1;
    for(;;){
        if(Object_type(args)!=Cell)return newInteger(value);
        if(Object_type(car(args))!=Integer)break;
        value /= Integer_value(car(args));
        args = cdr(args);
    }
    double fvalue = value;
    for(;;){
        if(Object_type(args)!=Cell)return newDouble(fvalue);
        if(Object_type(car(args))!=Double)break;
        fvalue /= Double_value(car(args));
        args = cdr(args);
    }
    fprintf(stderr,"ERROR:prim_plus\n");
    exit(1);
    return 0;
}

oop prim_equal(oop args,oop env){
    oop a = car(args);
    oop b = cadr(args);
    if(a==b)return t;
    int ta = Object_type(a);
    if(ta != Object_type(b))return nil;
    switch(ta){
        case Integer:{
            return (Integer_value(a)==Integer_value(b))?t:nil;
        }
        case Double:{
            return (Double_value(a)==Double_value(b))?t:nil;
        }
        default:
            break;
    }
    return nil;
}

oop prim_car(oop args,oop env){
    return car(car(args));
}
oop prim_cdr(oop args,oop env){
    return cdr(car(args));
}
oop prim_list_P(oop args,oop env){
    if(Object_type(car(args))==Cell)
        return t;
    return nil;
}

oop prim_cons(oop args,oop env){
    return newCell(car(args),cadr(args));
}
// 15.2
oop prim_eval(oop args,oop env){
    return eval(car(args),env);
}
oop prim_apply(oop args,oop env){
    return apply(car(args),cadr(args),env);
}

// 15.5
oop prim_islist(oop args,oop env){
    if(Object_type(car(args))==Cell)return t;
    return nil;
}
oop prim_isinteger(oop args,oop env){
    if(Object_type(car(args))==Integer)return t;
    return nil;
}
oop prim_isfloat(oop args,oop env){
    if(Object_type(car(args))==Double)return t;
    return nil;
}
oop prim_isstring(oop args,oop env){
    if(Object_type(car(args))==String)return t;
    return nil;
}
oop prim_issymbol(oop args,oop env){
    if(Object_type(car(args))==Symbol)return t;
    return nil;
}

oop prim_integer(oop args,oop env){
    oop obj = car(args);
    switch(Object_type(obj)){
        case Double:
            return newInteger((int)Double_value(obj));
        case String:{
            return newInteger(atoi(String_value(obj)));
        }
        default:
            break;
    }
    fprintf(stderr,"cannot convert type[prim_integer]\n");
    exit(1);
    return 0;
}

oop prim_float(oop args,oop env){
    oop obj = car(args);
    switch(Object_type(obj)){
        case Integer:
            return newDouble((double)Integer_value(obj));
        case String:
            return newDouble(atof(String_value(obj)));
        default:
            break;
    }
    fprintf(stderr,"cannot convert type[prim_float]\n");
    exit(1);
    return 0;
}
oop prim_symbol(oop args,oop env){    //asdf これあってるか？
    oop obj = car(args);
    if(Object_type(obj)==String){
        return newSymbol(String_value(obj));
    }
    fprintf(stderr,"cannot convert type[prim_symbol]\n");
    exit(1);
    return 0;
}
oop prim_string(oop args,oop env){
    oop obj = car(args);
    if(Object_type(obj)==String){
        return newString(Symbol_name(obj));
    }
    fprintf(stderr,"cannot convert type[prim_string]\n");
    exit(1);
    return 0;
}


oop prim_concat(oop args,oop env){
    oop a = car(args);
    oop b = cadr(args);
    switch(Object_type(a)){
        case Undefined:
            return b;
        case String:{//oK?
            if(b==nil)return a;
            return newString(strcat(String_value(a),String_value(b)));
        }
        case Symbol:{//oK?
            if(b==nil) return a;
            return newString(strcat(Symbol_name(a),Symbol_name(b)));
        }
        case Cell:{// (1 2) (3 4 5) || abc nil  // not good way
            if(b==nil)
                return a;
            oop list = nil;
            while(a!=nil){
                list = newCell(car(a),list);
                a = cdr(a);
            }
            while(b!=nil){
                list = newCell(car(b),list);
                b = cdr(b);
            }
            return revlist(list,nil);
        }
        default:
            break;
    }
    return 0;
}
//asdfj
oop prim_slice(oop args,oop env){
    oop obj = car(args);
    int a = Integer_value(cadr(args));
    int b = Integer_value(cadr(cdr(args)));
    oop c = cadr(car(car(args)));
    int k = 0;
    if(a>b){
        k = a;
        a = b;
        b = k;
    }
    switch(Object_type(obj)){
        case Cell:{
            oop list = nil;
            for(int i=0;i<a-1;i++){
                obj = cdr(obj);
            }
            for(int i=0;i<b-1;i++){
                list = newCell(car(obj),list);
                obj = cdr(obj);
            }
            if(k!=0)
                list = revlist(list,nil);
            return list;
        }
        case String:{
            char* value = strdup(String_value(obj));
            // if(k!=0){
            //     value = value[a-1,b-1];
            //     return newString(strrev(value));
            // }   
            value[b] = 0;         
            return newString(&value[a-1]);
        }
        case Symbol:{
            char* name = strdup(Symbol_name(obj));
            name[b]=0;
            return newSymbol(&name[a-1]);
        }
        default:
            break;
    }
    fprintf(stderr,"cannot get n th value[prim_slice]\n");
    exit(1);
    return nil;
}
oop prim_length(oop args,oop env){
    oop obj = car(args);
    switch(Object_type(obj)){
        case String:
            return newInteger(strlen(obj->String.value));
        case Symbol:
            return newInteger(strlen(obj->Symbol.name));
        case Cell:{
            int i = 0;
            while(obj!=nil){
                i++;
                obj = cdr(obj);
            }
            return newInteger(i);
        }
        default:
            fprintf(stderr,"this obj type doesn't have lenght[length]");
            exit(1);
    }
}
oop prim_nth(oop args,oop env){//(nth x n)
    oop obj = car(args);
    int n = Integer_value(cadr(args));
    switch(Object_type(obj)){
        case Cell:{
            for(int i=0;i<n-1;i++){
                obj = cdr(obj);
            }
            return car(obj);
        }
        case String:{
            char* value = strdup(String_value(obj));
            value[n]=0;
            return newString(&value[n-1]);
        }
        case Symbol:{
            char* name = strdup(Symbol_name(obj));
            name[n]=0;
            return newSymbol(&name[n-1]);
        }
        default:
            break;
    }
    fprintf(stderr,"cannot get n th value[prim_nth]\n");
    exit(1);
    return nil;
}
oop prim_set_nth(oop args,oop env){
    oop obj = car(args);
    int n = Integer_value(cadr(args));
    oop i = cadr(car(args));
    switch(Object_type(obj)){
        case Cell:{
        }
        case String:

        case Symbol:
        default:
            break;
    }
    fprintf(stderr,"cannot set nth[prim_set_nth]\n");
    exit(1);
    return 0;
}



/*////////////////////////////////////////////////////////

    SPEC FUNCION
    
////////////////////////////////////////////////////////*/
oop spec_define(oop args,oop env)
{
    oop name = car(args);
    if(Object_type(name)!=Symbol){
        fprintf(stderr,"name should be Symbol type[spec_define]\n");
        exit(1);
    }
    if(Object_type(name)==Cell){
        fprintf(stderr,"Cell[eval->sym_define:\n");
        exit(1);
    }
    oop value = cadr(args);
    value = eval(value,env);
    name->Symbol.value = value;
    define(name,value);
    return value;
}

oop spec_define_syntax(oop args,oop env)
{
    oop name = car(args);
    if(Object_type(name)!=Symbol){
        fprintf(stderr,"not symbol name in define-syntax\n");
        exit(1);
    }
    oop value = cadr(args);
    value = eval(value,env);
    
    oop ass = newCell(name,value);
    syntax = newCell(ass,syntax);
    return value;
}

oop spec_if(oop args,oop env)
{
    if(eval(car(args),env)==nil){
        return eval(caddr(args),env);
    }else{
        return eval(cadr(args),env);
    }
}

oop spec_while(oop args,oop env)
{
    while(eval(car(args),env)!=nil){
        oop arg = cdr(args);
        while(arg!=nil){
            eval(car(arg),env);
            arg = cdr(arg);
        }
    }
    return nil;
}

oop spec_quote(oop args,oop env)
{
    return car(args);
}
oop spec_unquote(oop args,oop env){
    return eval(cadr(args),env);
}

    // (quasiquote (1 (+ 2 3) (unquote (+ 4 5)) (+ 6 7)))
    // => (1 (+ 2 3) 9 (+ 6 7))
oop spec_quasiquote(oop args,oop env){
    if(Object_type(car(args))!=Cell)
        return car(args);

    oop list = nil;
    args = car(args);
    while(args!=nil){
        oop arg = car(args);//1, (+ 2 3), (unquote ...)

        if(Object_type(arg)==Cell){
            
            if(car(arg)==sym_unquote){
                printf("unquote:");
                arg = eval(cadr(arg),env);
            }

            if(car(arg)==sym_unquote_splicing){
                printf("spq:");
                oop alist = cadr(arg);
                alist = cdr(alist);
                while(cdr(alist)!=nil){
                    list = newCell(car(alist),list);
                    alist = cdr(alist);
                }
                arg = car(alist);
            }
        }
        list = newCell(arg,list);
        args = cdr(args);
    }
    return revlist(list,nil);
}
//(lambda (x) (* x x))
//(lambda args (....))
oop spec_lambda(oop args,oop env){
    return newClosure(car(args),cdr(args),env);
}

oop spec_print(oop args,oop env){
    print(args);
    while(args!=nil){
        print(eval(car(args),env));
        putchar(' ');
        args = cdr(args);
    }
    return nil;
}

oop spec_println(oop args,oop env){
    while(args!=nil){
        println(eval(car(args),env));
        args = cdr(args);
    }
    return nil;
}


// too long?
oop spec_let(oop args,oop env){
    //  (let ((n1 v1) (n2 v2) ...) e1 e2 ...)
    oop a_args = car(args); //((n1 v1) (n2 v2) ...) nx:para vx:valu
    oop values  = nil;
    oop parames = nil;
    while(a_args!=nil){
        oop paravalu = car(a_args);
        values = newCell(eval(cadr(paravalu),env),values);
        parames= newCell(car(paravalu),parames);
        a_args = cdr(a_args);
    }
    /*-using apply(), because inside spec function. but closure is not spec func...*/
    return apply(newClosure(parames,cdr(args),env),revlist(values,nil),env);
}

// add grcp14
oop spec_setq(oop args,oop env){
    oop association = assoc(car(args),env);
    oop value = eval(cadr(args),env);
    if(association==nil){
        oop name = car(args);
        if(name->Symbol.value==nil){
            fprintf(stderr,"undefined value:[in spec_setq]");
            exit(1);
        }
        define(name,value);
        return value;
    }
    Cell_setD(association,value);
    return value;
}


/*////////////////////////////////////////////////////////

    APPLY EVAL DEFINE

////////////////////////////////////////////////////////*/

oop apply(oop func,oop args,oop env){
    switch(Object_type(func)){
        case Primitive:
            return func->Primitive.function(args,env);
        case Special:
            return func->Special.function(args,env);
        case Closure:{
            oop newenv  = pairlist(Closure_parameters(func),args,Closure_environment(func));
            oop newfunc = func->Closure.expression;
            // printf("env: ");println(newenv);
            while(cdr(newfunc)!=nil){
                eval(car(newfunc),newenv);
                newfunc = cdr(newfunc);
            }
            return eval(car(newfunc),newenv);
        }
        default:
        break;
    }

	fprintf(stderr,"ERROR:end apply()\n");
	exit(1);
	return 0;
}


oop eval(oop exp,oop env){
	switch(Object_type(exp)){
		case ILLEGAL:
		case Undefined:
        case Integer:
        case Double:
        case String:
        case Primitive:
        case Special:
        case Closure:
			return exp;
		case Symbol:{
			oop list = assoc(exp,env);
			if(list==nil){
                oop value = exp->Symbol.value;
                if(value==nil){
                    fprintf(stderr,"is not defined value:[in eval symbol]");
                    print(exp);
                    exit(1);
                }
                return value;
			}
			return cdr(list);
		}
		case Cell:{
			oop func = eval(car(exp),env);
			oop args = cdr(exp);
            if(Object_type(func)!=Special)
                args = evlist(args,env);
			return apply(func,args,env);
		}
	}
    printf("EVAL ERROR:");
    return nil;
}

oop define(oop name, oop value){
    if(Object_type(name)!=Symbol){
        fprintf(stderr,"ERROR: name should be Symbol type[define]");
    }
    switch(Object_type(value)){


        case Primitive:{
            value->Primitive.name = name;
            break;
        }
        case Special:{
            value->Special.name = name;
            break;
        }
        case Closure:{
            value->Closure.name = name;
            break;
        }
        default:
            break;
    }
    name->Symbol.value = value;
    return value;
}

/*////////////////////////////////////////////////////////

    MAIN
    
////////////////////////////////////////////////////////*/

int main()
{
    nil        	= newObject(Undefined);
	t          	= newSymbol("t");

    sym_quote   = newSymbol("quote");
    sym_quasiquote = newSymbol("quasiquote");
    sym_unquote = newSymbol("unquote");
    sym_unquote_splicing = newSymbol("unquote-splicing");
    sym_lambda  = newSymbol("lambda");
	globals     = nil;
    syntax = nil;

    
    define(newSymbol("+"), newPrimitive(prim_plus));
    define(newSymbol("-"), newPrimitive(prim_minus));
    define(newSymbol("*"), newPrimitive(prim_multi));
    define(newSymbol("/"), newPrimitive(prim_divid));
    define(newSymbol("<"), newPrimitive(prim_less));
    define(newSymbol("="), newPrimitive(prim_equal));
    define(newSymbol("car"),newPrimitive(prim_car));
    define(newSymbol("cdr"),newPrimitive(prim_cdr));
    define(newSymbol("list?"),newPrimitive(prim_list_P));
    define(newSymbol("cons"),newPrimitive(prim_cons));
// 15.5
    define(newSymbol("list?"),newPrimitive(prim_islist));
    define(newSymbol("integer?"),newPrimitive(prim_isinteger));
    define(newSymbol("float?"),newPrimitive(prim_isfloat));
    define(newSymbol("string?"),newPrimitive(prim_isstring));
    define(newSymbol("symbol?"),newPrimitive(prim_issymbol));

    define(newSymbol("integer"),newPrimitive(prim_integer));
    define(newSymbol("float"),newPrimitive(prim_float));
    define(newSymbol("symbol"),newPrimitive(prim_symbol));
    define(newSymbol("string"),newPrimitive(prim_string));

    define(newSymbol("concat"),newPrimitive(prim_concat));
    define(newSymbol("slice"),newPrimitive(prim_slice));
    define(newSymbol("length"),newPrimitive(prim_length));
    define(newSymbol("nth"),newPrimitive(prim_nth));
    // define(newSymbol("set-nth"),newPrimitive(prim_set_nth));
//
    define(newSymbol("define"),newSpecial(spec_define));
    define(newSymbol("define-syntax"),newSpecial(spec_define_syntax));
    define(newSymbol("if"),    newSpecial(spec_if));
    define(newSymbol("while"), newSpecial(spec_while));

    define(newSymbol("quote"), newSpecial(spec_quote));
    define(newSymbol("quasiquote"),newSpecial(spec_quasiquote));//w15
    define(newSymbol("unquote"),newSpecial(spec_unquote));

    define(newSymbol("lambda"),newSpecial(spec_lambda));
    define(newSymbol("eval"), newPrimitive(prim_eval));
    define(newSymbol("apply"), newPrimitive(prim_apply));

    define(newSymbol("print"),  newSpecial(spec_print));
    define(newSymbol("println"),newSpecial(spec_println));
    define(newSymbol("let"),    newSpecial(spec_let));
    define(newSymbol("setq"),   newSpecial(spec_setq));

    for (;;) { // read-print loop
        oop obj = read();
        if (!obj) break;
        println(eval(obj,globals));
    }
    return 0;
}