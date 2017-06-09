#include <iostream>
using namespace std;
#include "huffman.h"

//frequences des lettres pour les mots français (source internet)
int FREQ[26] = { 942,   102,   264,   339,  1587,    95,   104,    77,
         841,    89,     0,   534,   324,   715,   514,   286,
         106,   646,   790,   726,   624,   215,     0,    30,
          24,    32};

vector<char> decode(Arbre arbre, bool* b, int m){
	vector<char> text;
	text.clear();
	Noeud node = arbre.noeud(arbre.racine()); 
	for(int i=0;i<m; ++i){
		
		if(b[i] == true){
			node = arbre.noeud(node.gauche);
		}else{
			node = arbre.noeud(node.droite);
		}
		if(node.droite == -1 || node.gauche == -1){
			text.push_back(node.c);
			node = arbre.noeud(arbre.racine());
		}
	}
	return text;
}


vector<bool> encode(Arbre arbre, char* str, int p){
	vector<vector<bool> > ref = arbre.getCode();
	vector<bool> b;

	for(int i=0;i<p;++i){
		int num = (int)(str[i] - 'a');
		b.insert(b.end(), ref[num].begin(), ref[num].end());
	}
	return b;
}



int main(int argc, char** argv){
	char alphabet[26] = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'};
	vector<int> H;
	for(int i=0;i<26;++i){
		H.push_back(FREQ[i]);
	}
	Arbre arbre(H);
	vector<vector<bool> > code = arbre.getCode();
	for(int i=0;i<code.size();++i){
		vector<bool> mot = code[i];
		cout<<alphabet[i]<<":  ";
		for(int j=0;j<mot.size();++j){
			cout<<mot[j];
		}
		cout<<endl;
	}
	string s = "texte";
	char* str = new char[s.size()];
	for(int i=0;i<s.size();++i){
		str[i] = s[i];
	}
	vector<bool> mot_code = encode(arbre, str, s.size());
	cout<<endl;
	cout<<"mot code:   ";
	for(int i=0;i<mot_code.size();++i){
		cout<<mot_code[i];
	}
	cout<<endl;
	return 0;
}