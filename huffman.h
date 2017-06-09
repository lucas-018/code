class Noeud {
public:
	char c;
	int count;
	int gauche, droite;
	Noeud(){}
	Noeud(char ch, int n, int g, int d){
		c = ch;
		count = n;
		gauche = g;
		droite = d;
	}
};

class Arbre{
	vector<Noeud> node;
	Arbre(){}
	void ajoute_feuille(char ch, int n){
		Noeud no(ch, n, -1,-1);
		node.push_back(no);
	}
	void fusionne(int i, int j){
		int n = node[i].count + node[j].count;
		Noeud parent('', n, i, j);
		node.push_back(parent);
	}
	int racine(){
		return node[node.size()-1];
	}
	Noeud noeud(int i){
		return node[i];
	}
};


vector<char> decode(Arbre arbre, bool* b, int m);