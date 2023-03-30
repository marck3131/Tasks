#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

vector<vector<vector<string>>> getLabyrinth(fstream* inputFile){
    vector<vector<vector<string>>> ans;
    while(!inputFile->eof()){
        vector<vector<string>> temp;
        string s;
        while(getline(*inputFile, s)){
            cout << s << endl;
            vector<string> line;
            if (s == "X") {
                break;
            }
            for(int i=0; i<s.size(); i++){
                line.push_back(string(1, s[i]));
            }
            temp.push_back(line);
        }
        ans.push_back(temp);
    }
    inputFile->close();
    return ans;
}
void printVector(vector<vector<string>> const &v){
    for(int i = 0; i < v.size(); i++){
        for(int j = 0; j < v[i].size(); j++){
            cout << v[i][j];
        }
        cout << endl;
    }
}
void writeVector(vector<vector<string>> const &v, int dist){
    string filename = HOME + (string)"/output.txt";
    ofstream out(filename, ios_base::app);
    out << dist << '\n';
    for(int i = 0; i < v.size(); i++){
        for(int j = 0; j < v[i].size(); j++){
            out << v[i][j];
        }
        out << endl;
    }
    out.close();

}
bool checkValid(vector<vector<string>> &v){
    bool top = false;
    bool bottom = false;
    for(int i = 0; i < v[0].size(); i++){
        if(v[0][i] == "."){
            top = true;
            break;
        }
    }

    for(int j = 0; j < v[v.size()-1].size(); j++){
        if(v[v.size()-1][j] == "."){
            bottom = true;
            break;
        }
    }

    return (top && bottom);

}
vector<pair<int,int>> getSources(vector<vector<string>> const &v){
    vector<pair<int,int>> sourceList;
    for(int i = 0; i < v[0].size(); i++){
        if(v[0][i] == "."){
            
            sourceList.push_back(make_pair(0, i));
        }
    }
    return sourceList;
}

vector<pair<int,int>> getDestinations(vector<vector<string>> const &v){
    vector<pair<int,int>> destinationList;
    for(int i = 0; i < v[v.size()-1].size(); i++){
        if(v[v.size()-1][i] == "."){
            
            destinationList.push_back(make_pair(v.size()-1, i));
        }
    }
    return destinationList;
}

bool isSafe(vector<vector<string>> &l, vector<vector<bool>> &v, int i, int j){
    if(i >= 0 && j >=0 && i<l.size() && j<l[0].size() && l[i][j] != "#" && v[i][j] != true){
        return true;
    }
    return false;
}

void findLongestPath(vector<vector<string>> &labyrinth, vector<vector<bool>> &visited, int s_r, int s_c, int d_r, int d_c, int &max_dist, int dist){
 
    if(labyrinth[s_r][s_c] == "#"){
        return;
    }

    if (dist > max_dist || max_dist == 0){
        labyrinth[s_r][s_c] = to_string(dist);
    }
     
    if(s_r == d_r && s_c == d_c){
        max_dist = max(dist, max_dist);
        return;
    }
    
    visited[s_r][s_c] = true;

    if(isSafe(labyrinth, visited, s_r - 1, s_c)){
        findLongestPath(labyrinth, visited, s_r - 1, s_c, d_r, d_c, 
        max_dist, dist + 1);
    }

    if(isSafe(labyrinth, visited, s_r - 1, s_c + 1)){
        findLongestPath(labyrinth, visited, s_r - 1, s_c + 1, d_r, d_c, 
        max_dist, dist + 1);
    }

    if(isSafe(labyrinth, visited, s_r - 1, s_c - 1)){
        findLongestPath(labyrinth, visited, s_r - 1, s_c - 1, d_r, d_c, 
        max_dist, dist + 1);
    }

    if(isSafe(labyrinth, visited, s_r, s_c + 1)){
        findLongestPath(labyrinth, visited, s_r, s_c + 1, d_r, d_c, 
        max_dist, dist + 1);
    } 

    if(isSafe(labyrinth, visited, s_r, s_c - 1)){
        findLongestPath(labyrinth, visited, s_r, s_c - 1, d_r, d_c, 
        max_dist, dist + 1);
    }

    if(isSafe(labyrinth, visited, s_r + 1, s_c)){
        findLongestPath(labyrinth, visited, s_r + 1, s_c, d_r, d_c, 
        max_dist, dist + 1);
    }

    if(isSafe(labyrinth, visited, s_r + 1, s_c - 1)){
        findLongestPath(labyrinth, visited, s_r + 1, s_c - 1, d_r, d_c, 
        max_dist, dist + 1);
    }

    if(isSafe(labyrinth, visited, s_r + 1, s_c + 1)){
        findLongestPath(labyrinth, visited, s_r + 1, s_c + 1, d_r, d_c, 
        max_dist, dist + 1);
    }

    visited[s_r][s_c] = false;
}

void createOutputLabyrinth(vector<vector<string>> &labyrinth, vector<pair<int, int>> &destinations, vector<pair<int, int>> &sources){
    if(labyrinth.size() == 0 || destinations.size() == 0 || sources.size() == 0){
        return;
    }
    int m = labyrinth.size();
    int n = labyrinth[0].size();

    int write_dist = 0;
    vector<vector<string>> write_laby = labyrinth;

    for(int i=0; i < destinations.size(); i++){
        for(int j=0; j< sources.size(); j++){
            vector<vector<bool>> visited;
            visited.resize(m, vector<bool>(n));
            vector<vector<string>> t_laby = labyrinth;
            int max_dist = 0;
            findLongestPath(t_laby, visited, sources[i].first, sources[i].second,
            destinations[j].first, destinations[j].second, max_dist, 0);
            max_dist++;        
            if(max_dist > write_dist){
                write_dist = max_dist;
                write_laby = t_laby;
            }
        }
    }
    if (write_dist == 1){
        writeVector(labyrinth, -1);
    }
    else{
        writeVector(write_laby, write_dist);
    }

}

int main(){
    fstream inputFile;
    string filename = HOME + (string)"/examples.txt";
    cout << filename << endl;
    inputFile.open(filename, ios::in);

    vector<vector<vector<string>>> labyrinths = getLabyrinth(&inputFile);

    for(int i = 0; i < labyrinths.size(); i++){
        vector<vector<string>> labyrinth = labyrinths[i];
        
        printVector(labyrinth);

        
        if(checkValid(labyrinth)){
           
            vector<pair<int, int>> destinations = getDestinations(labyrinth);   
            vector<pair<int, int>> sources = getSources(labyrinth);

            createOutputLabyrinth(labyrinth, destinations, sources);
        } else {
            
            writeVector(labyrinth, -1);
        }
    }

    inputFile.close();
    return 0;
}

