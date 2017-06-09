#include <iostream>
using namespace std;


vector<char> decode(Arbre arbre, bool* b, int m){
	vector<char> text;
	text.clear();
	node = arbre.noeud(arbre.racine()) 
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