const fs = require('fs');

function ASCII(binaryString) 
{
    return String.fromCharCode(parseInt(binaryString, 2));
}

class Node 
{
    constructor(symbol = '', weight = 0, parent = null, left = null, right = null) 
    {
        this.parent = parent;
        this.left = left;
        this.right = right;
        this.weight = weight;
        this.symbol = symbol;
    }
}

class Huffman 
{
    constructor() 
    {
        this.nyt = new Node('NYT');
        this.root = this.nyt;
        this.nodes = [];
        this.visited = Array(256).fill(null);
    }

    get_code(s, node, code = '') 
    {
        if (node.left === null && node.right === null) 
        {
            if(node.symbol===s)
            {
                return code
            }
            else
            {
                return ''
            }
        } 
        else 
        {
            let temp = '';

            if (node.left !== null) 
            {
                temp = this.get_code(s, node.left, code + '0');
            }

            if (!temp && node.right !== null) 
            {
                temp = this.get_code(s, node.right, code + '1');
            }

            return temp;
        }
    }

    get_largest_node(weight) 
    {
        for (let node of this.nodes) 
        {
            if (node.weight === weight) 
            {
                return node;
            }
        }
    }

    swap_nodes(first, second) 
    {
        let first_index=this.nodes.indexOf(first);
        let second_index=this.nodes.indexOf(second);
        [first_index,second_index]=[second_index,first_index];
        [this.nodes[first_index], this.nodes[second_index]] = [this.nodes[second_index], this.nodes[first_index]];

        [first.parent, second.parent] = [second.parent, first.parent];

        if (first.parent.left === second) 
        {
            first.parent.left = first;
        }
        else
        { 
            first.parent.right = first;
        }

        if (second.parent.left === first) 
        {
            second.parent.left = second;
        }
        else 
        {
            second.parent.right = second;
        }
    }

    insert(s) 
    {
        let node = this.visited[s];

        if (node === null || node === undefined) 
        {
            let new_node = new Node(s, 1);
            let new_parent = new Node('', 1, this.nyt.parent, this.nyt, new_node);

            new_node.parent = new_parent;
            this.nyt.parent = new_parent;

            if (new_parent.parent !== null) new_parent.parent.left = new_parent;
            else this.root = new_parent;

            this.nodes.push(new_parent);
            this.nodes.push(new_node);

            this.visited[s] = new_node;
            node = new_parent.parent;
        }
        
        while (node !== null) 
        {
            let largest = this.get_largest_node(node.weight);

            if (node !== largest && node !== largest.parent && largest !== node.parent) 
            {
                this.swap_nodes(node, largest);
            }

            node.weight++;
            node = node.parent;
        }
    }

    encode(character) 
    {
        let result = '';
        if (this.visited[character]) 
        {
            result = this.get_code(character, this.root);
        } 
        else 
        {
            result = this.get_code('NYT', this.root);
            result=result.concat(character.toString(2).padStart(8, '0'));
        }
        this.insert(character);
        return result;
    }

    decode(text) 
    {
        let output=Array();

        let symbol = ASCII(text.slice(0, 8));
        output.push(symbol.charCodeAt(0));
        this.insert(symbol);

        let node = this.root;
        let i = 8;
        while (i < text.length) 
        {
            node = text[i] === '0' ? node.left : node.right;
            symbol = node.symbol;

            if (symbol) 
            {
                if (symbol === 'NYT') 
                {
                    symbol = ASCII(text.slice(i + 1, i + 9));
                    i += 8;
                }

                output.push(symbol.charCodeAt(0));
                this.insert(symbol);
                node = this.root;
            }
            i++;
        }

        return output;
    }
    node_code(node)
    {
        let code='';
        while(node.parent!==null)
        {
            let p=node.parent;
            if (p.left===node)
            {
                code=code+'0';
            }
            else
            {
                code=code+'1';
            }
            node=p;
        }
        return code;
    }
    average_code_length()
    {
        let lengths=Array();
        let counter=0

        for(const symbol of this.visited)
        {
           if(symbol===null)
           {
                continue;
           }
           lengths.push(this.node_code(symbol).length);
           counter=counter+1;
        }
        return lengths.reduce((a, b) => a + b, 0)/counter;
    }
    entropy()
    {
        let entropy=0;
        for(const symbol of this.visited)
        {
            if(symbol===null)
            {
                continue;
            }
            entropy=entropy+symbol.weight*(-Math.log2(symbol.weight))
            //console.log(symbol.weight);
            //console.log(-Math.log2(symbol.weight)); 
        }
        entropy=entropy/this.root.weight;
        entropy=entropy+Math.log2(this.root.weight);
        console.log(entropy);
        if(entropy<0)
        {
            entropy=0;
        }
        return entropy;
    }
}

if (process.argv.length !== 5) 
{
    console.error('Usage: node index.js (decode|encode) [input] [output]');
    process.exit(1);
}

const mode = process.argv[2];
const input = process.argv[3];
const output = process.argv[4];

const huffman = new Huffman();
console.time('Wykonanie')
if(mode==='encode')
{
    fs.readFile(input,(error, buffer) => {
        if (error) {
            console.error(error);
            process.exit(1);
        }
        let result_temp="";
        let counter=1;
        for(byte of buffer)
        {
            result_temp=result_temp+huffman.encode(byte);
            counter=counter+1;
        }
        result=Array();
        padding=0;
        for(let i=0;i<Math.ceil(result_temp.length/8);i++)
        {
            temp=result_temp.slice(i*8,((i+1)*8));
            if(temp.length !==8)
            {
                padding=8-temp.length;
                temp=temp+"0".repeat(padding);
            }
            temp=parseInt(temp,2);
            result.push(temp);
        }
        result.unshift(padding);
        let final_result = Buffer.alloc(result.length);
        var writeStream = fs.createWriteStream(output);
        let offset=0;
        for(item of result)
        {
            final_result.writeUInt8(item,offset);
            offset=offset+1;
        }    
        fs.writeFile(output, final_result, () => {
            console.log('Kompresja ukonczona');
        });
        console.log("Średnia długość słowa kodowego: ", huffman.average_code_length());
        console.log("Współczynnik kompresji: ",counter*1.0/result.length);
        console.log("Entropia: ", huffman.entropy());
        console.timeEnd('Wykonanie');
    });
}
else
{
    let data="";
    fs.readFile(input,(error, buffer) => {
        if (error) {
            console.error(error);
            process.exit(1);
        }
        padding=buffer[0];

        for(let a=1;a<buffer.length;a++)
        {
            byte=buffer[a];
            for(let i=0;i<8;i++)
            {
                if((byte>>(7-i)) &0b1)
                {
                    data=data+"1";
                }
                else
                {
                    data=data+"0";
                }
            }
        }
        data=data.slice(0, -padding);
        result=huffman.decode(data);
        let final_result = Buffer.alloc(result.length);
        var writeStream = fs.createWriteStream(output);
        let offset=0;
        for(item of result)
        {
            final_result.writeUInt8(item,offset);
            offset=offset+1;
        }    
        fs.writeFile(output, final_result, () => {
            console.log('Kompresja ukonczona');
        });
        console.timeEnd('Wykonanie')
    });
}