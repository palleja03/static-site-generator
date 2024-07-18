You may want to make main.sh executable by running
```
chmod +x main.sh
```
^ same with test.sh

Considerations: 
 - Some tags should be depured when creating ParentNodes, nested blocks should be considered. e.g. multiple "p"
 - For the sake of simplicity, currently, nested nodes are not allowed. This requires consideration on the type of tags that can be nested.