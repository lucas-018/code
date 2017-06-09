#include <iostream>
using namespace std;
#include <vector>
#include <queue>

class Couple{
public:
	int ind;
	int freq;
	Couple(){}
	Couple(int i, int j){
		ind = i;
		freq = j;
	}
	bool operator<(const Couple C) const{
		return C.freq < freq;
	}
};

class Noeud {
public:
	char c;
	int count;
	int gauche;
	int droite;
	Noeud(){}
	Noeud(char ch, int n, int g, int d){
		c = ch;
		count = n;
		gauche = g;
		droite = d;
	}
};

class Arbre{
public:
	vector<Noeud> node;
	priority_queue<Couple> E;
	Arbre(){}
	Arbre(vector<int> H){
		char alphabet[26] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
		node.clear();
		for(int i=0;i<H.size();++i){
			ajoute_feuille(alphabet[i], H[i]);
			Couple C(i, H[i]);
			E.push(C);
		}
		while(E.size()>1){
			Couple C1 = E.top();
			E.pop();
			Couple C2 = E.top();
			E.pop();
			fusionne(C1.ind, C2.ind);
			int new_ind = node.size() -1;
			int new_freq = C1.freq + C2.freq;
			Couple C(new_ind, new_freq);
			E.push(C);
		}
	}
	void ajoute_feuille(char ch, int n){
		Noeud no(ch, n, -1,-1);
		node.push_back(no);
	}
	void fusionne(int i, int j){
		int n = node[i].count + node[j].count;
		Noeud parent(' ', n, i, j);
		node.push_back(parent);
	}
	vector<vector<bool> > parcourt(int ind, vector<bool> prefixe, vector<vector<bool> > code){
		Noeud no = noeud(ind);
		if(no.droite == -1 || no.gauche== -1){
			vector<bool> this_code = prefixe;
			code[ind] = this_code;
		}else{
			prefixe.push_back(true);
			int g = no.gauche;
			code = parcourt(g, prefixe, code);
			prefixe.pop_back();
			prefixe.push_back(false);
			int d = no.droite;
			code = parcourt(d, prefixe, code);
			prefixe.pop_back();
		}
		return code;
	}
	int racine(){
		return node.size()-1;
	}
	Noeud noeud(int i){
		return node[i];
	}
	vector<vector<bool> > getCode(){
		vector<vector<bool> > code;
		for(int i=0;i<26;++i){
			vector<bool> b;
			code.push_back(b);
		}
		int ind = racine();
		vector<bool> prefixe;
		prefixe.clear();
		code = parcourt(ind, prefixe, code);
		return code;
	}
};


vector<char> decode(Arbre arbre, bool* b, int m);
vector<bool> encode(Arbre arbre, char* str, int p);
