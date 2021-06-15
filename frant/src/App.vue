<template>
    <div class="demo-split">
        <Button type="primary" v-on:click="transhandler">翻译</Button>
        <!--<Button type="primary" v-on:click="changer">{{change_text}}</Button>-->
        <Split v-model="split1" :mode="mode">
            <div :slot="artical_state" class="demo-split-pane">

                <MarkdownPro
                       autoSave=true
                       v-model="text"
                       ref="markchange"
                       height="mark_heigh"
                       bordered=false
                       @on-save="handleOnSave"
               />
            </div>
            <div :slot="word_state" class="demo-split-pane" id="word_list" >

                <Tag class="tag" v-for="(item, index) in Tags"
                     :key="item.id"
                     :name="index"
                     :id="item.id">{{item.text}}
                </Tag>

            </div>

        </Split>
    </div>
</template>
<script>
    import {Split} from 'view-design'
    // import Markdown from 'vue-meditor';
    import { MarkdownPro } from 'vue-meditor'
    // import { MarkdownPreview } from 'vue-meditor'
    import Highlighter from 'web-highlighter';
    import LocalStore from './local.store';
    import Vue from 'vue'
    var query = window.location.search.substring(1);
    const store = new LocalStore();
    // 不高亮 pre&code 元素
    const highlighter = new Highlighter({
        wrapTag: 'i',
        exceptSelectors: ['.my-remove-tip', 'pre', 'code']
    });
    const log = console.log.bind(console, '[highlighter]');

    /**
     * create a delete tip
     */
    const createTag = (top, left, id, text) => {
        window.add({
            'id':id,
            'text':text
        });

        // $span.style.left = `${left - 20}px`;
        // $span.style.top = `${top - 25}px`;
        // $span.dataset['id'] = id;
        // $span.textContent = 'delete';
        // $span.classList.add('my-remove-tip');
        // $span.appendChild(tag);
    };

    /**
     * toggle auto highlighting & button status
     */
// const switchAuto = auto => {
//     auto === 'on' ? highlighter.run() : highlighter.stop();
//     const $btn = document.getElementById('js-highlight');
//     if (auto === 'on') {
//         $btn.classList.add('disabled');
//         $btn.setAttribute('disabled', true);
//     }
//     else {
//         $btn.classList.remove('disabled');
//         $btn.removeAttribute('disabled');
//     }
// };

    function getPosition($node) {
        let offset = {
            top: 0,
            left: 0
        };
        while ($node) {
            offset.top += $node.offsetTop;
            offset.left += $node.offsetLeft;
            $node = $node.offsetParent;
        }
        return offset;
    }

    /**
     * highlighter event listener
     */
    highlighter
        .on(Highlighter.event.CLICK, ({id}) => {
            log('click -', id);
            highlighter.remove(id)
            // $ele.parentNode.removeChild($ele);
            window.removeById(id)
        })
        .on(Highlighter.event.HOVER, ({id}) => {
            log('hover -', id);
            highlighter.addClass('highlight-wrap-hover', id);
        })
        .on(Highlighter.event.HOVER_OUT, ({id}) => {
            log('hover out -', id);
            highlighter.removeClass('highlight-wrap-hover', id);
        })
        .on(Highlighter.event.CREATE, ({sources}) => {
            log('create -', sources);
            sources.forEach(s => {
                const position = getPosition(highlighter.getDoms(s.id)[0]);
                createTag(position.top, position.left, s.id, s.text);
            });
            sources = sources.map(hs => ({hs}));
            store.save(sources);
            var url = `${window.backendUrl}/word_save/${query}`;
            const source = sources[0].hs
            const data = {
                text:source.text
            }
            Vue.http.post(url, data, {emulateJSON:true}).then(res =>{
                if(res.body == 'ok'){
                    console.log(res)
                }
            })
            log('all:::', store.getAll())
        })
        .on(Highlighter.event.REMOVE, ({ids}) => {
            log('remove -', ids);
            ids.forEach(id => store.remove(id));
        });
    highlighter.hooks.Render.WrapNode.tap(function (id, node,) {
        // 生成 id
        // <ruby>
        // 漢 <rt> ㄏㄢˋ </rt>
        // </ruby>
        var text = node.innerText;
        var ruby = document.createElement('ruby');
        var rt = document.createElement("rt");
        node.innerText = '';
        ruby.innerText = text;

        var url = `${window.backendUrl}/search_word/${query}`;
        Vue.http.post(url, {text: text}, {emulateJSON: true}).then(res => {
            const {status, result} = res.body;
            var phonetic = 'sorry';
            if (status == 'ok') {
                phonetic = result.phonetic
            }
            rt.innerText = `/${phonetic}/`;
            rt.classList.add("phonetic");
            ruby.appendChild(rt);
            node.appendChild(ruby, text);
            return node;
        });
    })

    /**
     * avoid re-highlighting the existing selection
     */
    function getIds(selected) {
        if (!selected || !selected.$node || !selected.$node.parentNode) {
            return [];
        }
        return [
            highlighter.getIdByDom(selected.$node.parentNode),
            ...highlighter.getExtraIdByDom(selected.$node.parentNode)
        ].filter(i => i)
    }
    function getIntersection(arrA, arrB) {
        const record = {};
        const intersection = [];
        arrA.forEach(i => record[i] = true);
        arrB.forEach(i => record[i] && intersection.push(i) && (record[i] = false));
        return intersection;
    }
    highlighter.hooks.Render.SelectedNodes.tap((id, selectedNodes) => {
        selectedNodes = selectedNodes.filter(n => n.$node.textContent);
        if (selectedNodes.length === 0) {
            return [];
        }

        const candidates = selectedNodes.slice(1).reduce(
            (left, selected) => getIntersection(left, getIds(selected)),
            getIds(selectedNodes[0])
        );
        for (let i = 0; i < candidates.length; i++) {
            if (highlighter.getDoms(candidates[i]).length === selectedNodes.length) {
                return [];
            }
        }

        return selectedNodes;
    });

    highlighter.hooks.Serialize.Restore.tap(
        source =>  log('Serialize.Restore hook -', source)
    );

    highlighter.hooks.Serialize.RecordInfo.tap(() => {
        const extraInfo = Math.random().toFixed(4);
        log('Serialize.RecordInfo hook -', extraInfo)
        return extraInfo;
    });

    /**
     * retrieve from local store
     */
    const storeInfos =  store.getAll();
    storeInfos.forEach(
        ({hs}) => {
            highlighter.fromStore(hs.startMeta, hs.endMeta, hs.text, hs.id, hs.extra)
        }
    );

    // let autoStatus;
    // document.querySelectorAll('[name="auto"]').forEach($n => {
    //     if ($n.checked) {
    //         autoStatus = $n.value;
    //     }
    // });
    // switchAuto(autoStatus);

    document.addEventListener('click', e => {
        const $ele = e.target;

        // delete highlight
        if ($ele.classList.contains('my-remove-tip')) {
            const id = $ele.dataset.id;
            log('*click remove-tip*', id);
            highlighter.removeClass('highlight-wrap-hover', id);
            highlighter.remove(id);
            $ele.parentNode.removeChild($ele);
        }
        // toggle auto highlighting switch
        // else if ($ele.getAttribute('name') === 'auto') {
        //     const val = $ele.value;
        //     if (autoStatus !== val) {
        //         // switchAuto(val);
        //         autoStatus = val;
        //     }
        // }
        // highlight range manually
        else if ($ele.id === 'js-highlight') {
            const selection = window.getSelection();
            if (selection.isCollapsed) {
                return;
            }
            highlighter.fromRange(selection.getRangeAt(0));
            window.getSelection().removeAllRanges();
        }
    });

    let hoveredTipId;
    document.addEventListener('mouseover', e => {
        const $ele = e.target;
        // toggle highlight hover state
        if ($ele.classList.contains('my-remove-tip') && hoveredTipId !== $ele.dataset.id) {
            hoveredTipId = $ele.dataset.id;
            highlighter.removeClass('highlight-wrap-hover');
            highlighter.addClass('highlight-wrap-hover', hoveredTipId);
        }
        else if (!$ele.classList.contains('my-remove-tip') && !$ele.classList.contains('highlight-mengshou-wrap')) {
            highlighter.removeClass('highlight-wrap-hover', hoveredTipId);
            hoveredTipId = null;
        }
    });
    console.log(query);
    highlighter.run();
    

    export default {
        name: "markdown",
        components: {
            // Markdown,
            MarkdownPro,
            Split
        },
        mounted() {
        // methods里面定义的方法, 需要赋值给window
            window.add = this.add;
            // window.remove = this.remove;
            window.removeById = this.removeById;
            window.backendUrl = 'http://127.0.0.1:8888'
            var url = `${window.backendUrl}/read/${query}`;
            this.$http.get(url).then(res =>{
                this.text = res.body
            })
            // window.createElement = $createElement()
        },
        // updated: function() {
        //     // this.$refs.markchange.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;')
        //     // console.log(1234567)
        //     const data = store.getAll()
        //     this.Tags = data.slice(1,data.length)
        // },

        data() {
            return {
                split1: 0.9,
                transhandler:this.translation,
                text:'解析中',
                show: true,
                mark_heigh:'2000',
                change_text: '上下切换',
                mode: 'horizontal',
                artical_state: 'left',
                word_state: 'right',
                Tags:[],
                Tags_index:[],
                highlighter:highlighter
            };
        },
        methods: {
            translation() {
                console.log('==============in translations==============');
                var url = `${window.backendUrl}/get_trans/${query}`;
                var url2 = `${window.backendUrl}/get_words/${query}`;
                Vue.http.get(url2).then(res=>{
                    res = res.body
                    const words = res.result;

                    this.text += '\n---\n';
                    for (var i of words) {
                        var t = '`' + `${i}` + '` ';
                        this.text += t
                    }

                    this.text += '\n\n---\n';

                    this.text+='\n| 字段        | 解释                                                       |\n' +
                    '| ----------- | ---------------------------------------------------------- |\n' +
                    '| word        | 单词名称                                                   |\n' +
                    '| phonetic    | 音标，以英语英标为主                                       |\n' +
                    '| definition  | 单词释义（英文），每行一个释义                             |\n' +
                    '| translation | 单词释义（中文），每行一个释义                             |\n' +
                    '| pos         | 词语位置，用 "/" 分割不同位置                              |\n' +
                    '| collins     | 柯林斯星级                                                 |\n' +
                    '| oxford      | 是否是牛津三千核心词汇                                     |\n' +
                    '| tag         | 字符串标签：zk/中考，gk/高考，cet4/四级 等等标签，空格分割 |\n' +
                    '| bnc         | 英国国家语料库词频顺序                                     |\n' +
                    '| frq         | 当代语料库词频顺序                                         |\n' +
                    '| exchange    | 时态复数等变换，使用 "/" 分割不同项目，见后面表格          |\n' +
                    '| detail      | json 扩展信息，字典形式保存例句（待添加）                  |\n' +
                    '| audio       | 读音音频 url （待添加）                                    |\n\n'

                this.text += '| 类型 | 说明                                                       |\n' +
                    '| ---- | ---------------------------------------------------------- |\n' +
                    '| p    | 过去式（did）                                              |\n' +
                    '| d    | 过去分词（done）                                           |\n' +
                    '| i    | 现在分词（doing）                                          |\n' +
                    '| 3    | 第三人称单数（does）                                       |\n' +
                    '| r    | 形容词比较级（-er）                                        |\n' +
                    '| t    | 形容词最高级（-est）                                       |\n' +
                    '| s    | 名词复数形式                                               |\n' +
                    '| 0    | Lemma，如 perceived 的 Lemma 是 perceive                   |\n' +
                    '| 1    | Lemma 的变换形式，比如 s 代表 apples 是其 lemma 的复数形式 |\n\n'
                });

                Vue.http.get(url).then(res=>{
                    const result = res.body.result;

                    this.text += '\n|单词|解释|\n' +
                        '|---|---|\n'
                    result.map(item=>{
                        if(item != null) {
                            this.text += `|${item['word']}|${item['translation'].replace(/\n/g,"<br>")}|\n`
                        }
                    })

                    this.text += '\n'
                    result.map(item=>{
                        if(item != null){
                            this.text += '```\n';
                            for(var i in item){
                                if(i == 'id' || i == 'sw' || i == 'audio' || i == 'phonetic'){
                                    console.log(i)
                                } else {
                                    this.text += `${i}: ${item[i]}\n`
                                }
                            }
                            this.text += '```\n'
                        }

                    })
                })
            },
            changer() {
                const text = this.change_text;
                if(text == '上下切换'){
                    this.change_text = '左右切换'
                    this.mode = 'vertical'
                    this.artical_state = 'bottom'
                    this.word_state = 'top'

                }else{
                    this.change_text = '上下切换'
                    this.mode = 'horizontal'
                    this.artical_state = 'left'
                    this.word_state = 'right'
                }
            },
            handleOnSave ({value, theme}) {
                var url = `${window.backendUrl}/mark_save/${query}`;
                console.log(theme)
                this.$http.post(url, {text:value}, {emulateJSON:true}).then(res =>{
                    console.log(res.body)
            })
            },
            //点击新增子组件
            add(tag){
                        this.Tags_index[tag.id] = this.Tags.length;
                        this.Tags.push(tag)
            },
            // //删除子组件
            remove(n){
                this.Tags.splice(n,1);
            },
            removeById(id){
                var url = `${window.backendUrl}/word_del/${query}`;
                this.$http.post(url, {id:id}, {emulateJSON:true}).then(res =>{
                    if(res.body == 'ok'){
                        this.remove(this.Tags_index[id])
                    }
                })
            }
        }
    }
</script>
<style>
    .phonetic {
        font-size: 15px;
    }
    .highlight-mengshou-wrap {
        background: #ff9;
        cursor: pointer;
        font-weight: bold;
    }
    .demo-split Button{
        margin: 10px;
    }
    .demo-split{
        height: 1150px;
        /*overflow: hidden;*/
        border: 1px solid #dcdee2;
    }
    .demo-split-pane{
        padding: 10px;
    }
    .demo-split-pane .tag {
        user-select: none;
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
    }
    h1:first-child {
        color: #3c86c7;
        padding-bottom: 0;
    }

    h1 + blockquote {
        box-shadow: inset 5px 0 #ddd;
    }

    h1 + blockquote p {
        margin-top: 10px;
        color: #aaa;
        margin-bottom: 40px;
    }

    main .highlight-wrap-hover {
        background: #f7aaaa;
    }

    .my-remove-tip {
        box-sizing: border-box;
        position: absolute;
        border: 1px solid #fff;
        border-radius: 3px;
        height: 20px;
        width: 40px;
        color: #fff;
        background: #444;
        text-align: center;
        font-size: 12px;
        cursor: pointer;
        line-height: 18px;
        overflow: visible;
    }

    .my-remove-tip::after {
        content: '';
        position: absolute;
        left: 16px;
        bottom: -4px;
        border-color: #444 transparent transparent;
        border-width: 4px 4px 0;
        border-style: solid;
        height: 0;
        width: 0;
    }

    .op-panel {
        box-sizing: border-box;
        padding: 1px 5px 6px 8px;
        position: fixed;
        top: 50px;
        left: 15px;
        background: rgba(0, 0, 0, .1);
        border-radius: 3px;
        border: 1px dashed #aaa;
    }

    .op-panel a {
        position: absolute;
        right: 10px;
        bottom: 12px;
        height: 18px;
        width: 18px;
        opacity: .7;
    }

    .op-panel a:hover {
        opacity: 1;
    }

    .op-panel svg {
        height: 18px;
        width: 18px;
    }

    .op-panel input[type="radio"] {
        opacity: 1;
        width: auto;
        position: static;
        line-height: normal;
        height: 15px;
        vertical-align: middle;
        margin-right: 5px;
    }

    .op-panel .op-name {
        margin-right: 0;
    }

    .op-panel label {
        font-size: 12px;
        margin-right: 2px;
    }

    .op-panel .op-btn {
        display: block;
        font-size: 12px;
    }

    .op-panel .op-btn.disabled {
        cursor: not-allowed;
    }

    @media screen and (max-width: 1150px) {
        main {
            padding: 0 15px;
            overflow-x: hidden;
        }

        .op-panel {
            right: 5vw;
            bottom: 5vh;
            left: auto;
            top: auto;
            background-color: rgba(0, 0, 0, .9);
            color: #fff;
        }
    }
</style>