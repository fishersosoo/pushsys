/**
 * Created by gzs10558 on 2017/7/27.
 */
var $table = $('#table'),
    $add = $('#addMessage'),
    $peopleTable = $("#peopleList");
Date.prototype.pattern = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours() % 12 == 0 ? 12 : this.getHours() % 12, //小时
        "H+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    var week = {
        "0": "/u65e5",
        "1": "/u4e00",
        "2": "/u4e8c",
        "3": "/u4e09",
        "4": "/u56db",
        "5": "/u4e94",
        "6": "/u516d"
    };
    if (/(y+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    if (/(E+)/.test(fmt)) {
        fmt = fmt.replace(RegExp.$1, ((RegExp.$1.length > 1) ? (RegExp.$1.length > 2 ? "/u661f/u671f" : "/u5468") : "") + week[this.getDay() + ""]);
    }
    for (var k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }
    return fmt;
};


var Today = new Date();
var Yesterday = new Date();
Yesterday.setDate(Yesterday.getDate() - 1);
$("#date").val((Yesterday.pattern("yyyy-MM-dd")));

function loadPeopleList(val) {
    //加载联系人列表
    $.get(
        "/people_group/",
        {},
        function (data) {
            if (data["errmsg"]) {
                alert(data["errmsg"])
                return;
            }
            select = $("#group");
            select.empty();
            for (i = 0; i < data.length; ++i) {
                group = data[i];
                select.append("<option>" + group["group_name"] + "</option>");
                $("#group option:last").data("people_list", group["people_list"]);
            }
            select.val(val);
        }
    )
}

function initPeopleTable() {
    $peopleTable.bootstrapTable({
        uniqueId: "name",
        columns: [
            {
                field: "name",
                title: "姓名",
                editable: true,
                align: 'center',
            },
            {
                field: "phone",
                title: "手机",
                editable: true,
                align: 'center',
            },
            {
                field: 'delete',
                title: '删除',
                align: 'center',
                events: deletePeopleEvents,
                formatter: deletePeopleFormatter
            }
        ]
    })
    ;
    //修改联系人信息保存
    $peopleTable.on('editable-save.bs.table', function (e, field, row, old, $el) {
        if (field == "name") {
            peoplelist = $peopleTable.bootstrapTable('getData');
            for (i = 0; i < peoplelist.length; ++i) {
                if (peoplelist[i]["name"] == row["name"] && peoplelist[i] != row) {
                    alert("重复联系人");
                    // $peopleTable.bootstrapTable("removeByUniqueId", row["name"]);
                }
            }
        }
    });
}

initSubTable = function initNormTable(index, row, $detail) {
    // alert();
    var parentid = row["_id"];
    var cur_table = $detail.html('' +
        '<div id="tool_' + parentid + '">' +
        '<button id="addNorm" class="btn btn-default">' +
        ' <i class="glyphicon glyphicon-plus"></i> Add' +
        '</button>' +
        '</div>' +
        '<table class="table table-striped" data-editable-mode="inline"></table>'
    ).find('table');
    var addButton = $detail.find(" button");
    $(cur_table).attr("id", "sub_" + parentid);
    $(cur_table).data("parentid", parentid);
    $(addButton).data("parentid", parentid);
    $(cur_table).bootstrapTable({
        url: '/norm_list/',
        method: "get",
        queryParams: {"belong_message": parentid},
        uniqueId: "_id",
        toolbar: "#tool_" + parentid,
        search: true,
        showRefresh: true,
        showToggle: true,
        showColumns: true,
        rowAttributes: function (row, index) {
            return {
                class: 'active'
            };
        },
        columns: [
            {
                field: "_id",
                title: "ID",
                sortable: true,
                editable: true,
                align: 'center',
                visible: false
            },
            {
                field: 'name',
                title: '发送指标名称',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'module',
                title: 'APP来源module',
                sortable: false,
                editable: false,
                align: 'center',
                visible: false
            },
            {
                field: 'template_id',
                title: 'APP来源模板',
                sortable: false,
                editable: false,
                align: 'center'
            },
            {
                field: 'terminal_id',
                title: 'APP来源终端',
                sortable: false,
                editable: false,
                align: 'center'
            },
            {
                field: 'room_id',
                title: 'APP来源房间',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'app_name',
                title: 'APP指标名称',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'table_name',
                title: '来源表名',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'field',
                title: '来源字段',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'threshold',
                title: '警告阈值',
                sortable: true,
                editable: true,
                align: 'center'
            },
            {
                field: 'incharge',
                title: '数据表负责人',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'phone',
                title: '负责人电话',
                sortable: false,
                editable: true,
                align: 'center'
            },
            {
                field: 'modify',
                title: '操作',
                align: 'center',
                events: modifyNormEvents,
                formatter: modifyNormFormatter
            }
        ]

    })
    $(addButton).on('click', function (e) {
        // alert(this);
        body = $("#newNormModal")
        input_fields = $(body.find("input"));
        for (var i = 0; i < input_fields.length; ++i) {
            field = $(input_fields[i]);
            field.val("");
        }
        select_fields = $(body.find("select"));
        for (var i = 0; i < select_fields.length; ++i) {
            field = $(select_fields[i]);
            // alert(field.attr("id"));
            if (field.attr("id") == "module") {
                // alert($(this).data("parentid"))
                // alert($table.bootstrapTable("getRowByUniqueId", $(this).data("parentid")))
                field.val($table.bootstrapTable("getRowByUniqueId", $(this).data("parentid"))["module"]);
            }
        }
        $("#newNormModal").modal("show");
        $("#editNormSave").hide();
        $("#newNormSave").show();
        $("#newNormSave").data("parentid", $(this).data("parentid"));
        $("#newNormSave").unbind();
        $("#newNormSave").on('click', function (e) {
            // alert("newNormSave");
            data = {};

            input_fields = $(body.find("input"));
            for (var i = 0; i < input_fields.length; ++i) {
                field = $(input_fields[i]);
                data[field.attr("id")] = field.val();
            }
            select_fields = $(body.find("select"));
            for (var i = 0; i < select_fields.length; ++i) {
                field = $(select_fields[i]);
                data[field.attr("id")] = field.val();
            }
            data["belong_message"] = $("#newNormSave").data("parentid");
            // alert(JSON.stringify(data));
            $.post(
                "/norm/",
                data,
                function (data, textStatus, jqXHR) {
                    if (data["errmsg"]) {
                        alert(data["errmsg"])
                        return;
                    }
                    cur_table.bootstrapTable("prepend", data);
                }
            )
        });
    });
    return cur_table;
}

function initTable() {
    $table.bootstrapTable({
        height: getHeight(),
        columns: [
            [{
                field: '_id',
                title: 'ID',
                sortable: true,
                editable: true,
                align: 'center',
                visible: false
            },
                {
                    field: 'name',
                    title: '消息名称',
                    sortable: true,
                    editable: true,
                    align: 'center'
                }, {
                field: 'app',
                title: '产品',
                sortable: true,
                align: 'center'
            }, {
                field: 'module',
                title: '模块',
                sortable: true,
                align: 'center'
            }, {
                field: 'desc',
                title: '添加说明与否',
                sortable: true,
                align: 'center',
                editable: true
            },
                {
                    field: 'preview',
                    title: '预览',
                    align: 'center',
                    events: previewEvents,
                    formatter: previewFormatter
                },
                {
                    field: 'send_me',
                    title: '发给自己',
                    align: 'center',
                    events: send_meEvents,
                    formatter: send_meFormatter
                },
                {
                    field: 'send_others',
                    title: '发给负责人',
                    align: 'center',
                    events: send_othersEvents,
                    formatter: send_othersFormatter
                }, {
                field: 'timer',
                title: '定时执行',
                align: 'center',
                visible: false
                // events: operateEvents,
                // formatter: operateFormatter
            },
                {
                    field: 'operate',
                    title: '操作',
                    align: 'center',
                    events: operateEvents,
                    formatter: operateFormatter
                }
            ]
        ]
    });
    // 加载超时动作
    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);

    //点击详情的响应
    $table.on('expand-row.bs.table', function (e, index, row, $detail) {
        subTable = initSubTable(index, row, $detail);
        $(subTable).on('editable-save.bs.table', function (e, field, row, old, $el) {
            // alert("edit subtable");
            var data = {};
            data["_id"] = row["_id"];
            data[field] = row[field];
            $.post("/norm/",
                data,
                function (data, textStatus, jqXHR) {
                    if (data["errmsg"]) {
                        alert(data["errmsg"])
                        return;
                    }
                },
                "json")
            e.stopPropagation();
        });
        $(subTable).on('editable-shown.bs.table', function (editable, field, row, $el) {
            $(subTable).bootstrapTable("resetWidth");
        });
    });
    $table.on('all.bs.table', function (e, name, args) {
        console.log(name, args);
    });
    $(window).resize(function () {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
    $table.on('editable-save.bs.table', function (e, field, row, old, $el) {
        var data = {};
        data["_id"] = row["_id"];
        data[field] = row[field];
        $.post("/message/",
            data,
            function (data, textStatus, jqXHR) {
                if (data["errmsg"]) {
                    alert(data["errmsg"])
                    return;
                }
            },
            "json")

    });
}

function getIdSelections() {
    return $.map($table.bootstrapTable('getSelections'), function (row) {
        return row.id
    });
}

function responseHandler(res) {
    $.each(res.rows, function (i, row) {
        row.state = $.inArray(row.id, selections) !== -1;
    });
    return res;
}

function detailFormatter(index, row) {
    var html = [];
    $.each(row, function (key, value) {
        html.push('<p><b>' + key + ':</b> ' + value + '</p>');
    });
    return html.join('');
}

//发给自己显示内容
function send_meFormatter(value, row, index) {
    return [
        '<a class="send_me" href="javascript:void(0)" title="send_me">',
        '<i class="glyphicon glyphicon-send"></i>',
        '</a>  '
    ].join('');
}

//发给负责人显示内容
function send_othersFormatter(value, row, index) {
    return [
        '<a class="send_others" href="javascript:void(0)" title="send_others">',
        '<i class="glyphicon glyphicon-user"></i>',
        '</a>  ',
    ].join('');
}

//预览消息列显示内容
function previewFormatter(value, row, index) {
    return [
        '<a class="preview" href="javascript:void(0)" title="预览">',
        '<i class="glyphicon glyphicon-option-horizontal"></i>',
        '</a>  '
    ].join('');
}

function deletePeopleFormatter(value, row, index) {
    return [
        '<a class="remove" href="javascript:void(0)" title="删除">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}

//修改指标显示内容
function modifyNormFormatter(value, row, index) {
    return [
        '<a class="edit" href="javascript:void(0)" title="修改">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>  ',
        '<a class="remove" href="javascript:void(0)" title="删除">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}

//操作列显示内容
function operateFormatter(value, row, index) {
    return [
        // '<a class="time" href="javascript:void(0)" title="time">',
        // '<i class="glyphicon glyphicon-time"></i>',
        // '</a>  ',
        '<a class="edit" href="javascript:void(0)" title="修改">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>  ',
        '<a class="remove" href="javascript:void(0)" title="删除">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}

//操作列事件响应
window.operateEvents = {
    //修改消息
    'click .edit': function (e, value, row, index) {
        initPeopleTable();
        loadApps()
        var people_list = JSON.parse(row["people_list"]);
        var people = [];
        for (k in people_list) {
            people.push({"name": k, "phone": people_list[k]});
        }
        loadPeopleList("");
        $peopleTable.bootstrapTable("load", people);
        $("#messageName").val(row["name"]);
        $("#messageApp").val(row["app"]);
        $("#messageModule").val(row["module"]);
        $("#messageDesc").val(row["desc"]);
        $("#newMessageModal").data("index", index);
        $("#newMessageModal").data("row", row);
        $("#group_name").val("");

        $("#newMessageModal").modal("show");
        $("#editMessageSave").show();
        $("#newMessageSave").hide();
        // alert('You click edit action, row: ' + JSON.stringify(row));
    },
    'click .remove': function (e, value, row, index) {
        $.post(
            "/message_delete/",
            {
                "_id": row["_id"]
            },
            function (data, textStatus, jqXHR) {
                if (data["errmsg"]) {
                    alert(data["errmsg"])
                    return;
                }
                $table.bootstrapTable("removeByUniqueId", row["_id"]);
            }
        );
    },
    'click .time': function (e, value, row, index) {
        //定时执行设置
        if (row["timer"] !== "") {
            $.post(
                "/job_del/",
                {
                    "message_id": row["_id"]
                },
                function (data, textStatus, jqXHR) {
                    $table.bootstrapTable("updateCell", {'index': index, "field": "timer", "value": ""})
                }
            );
        }
        else {
            if ($("#time").val() === "") {
                alert("请输入时间")
                return
            }
            $.post(
                "/job_add/",
                {
                    "message_id": row["_id"],
                    "run_time": $("#time").val()
                },
                function (data, textStatus, jqXHR) {
                    $table.bootstrapTable("updateCell", {'index': index, "field": "timer", "value": data["run_time"]})
                }
            );
        }
    }
};
window.send_meEvents = {
    'click .send_me': function (e, value, row, index) {
        if ($("#date").val() === "") {
            alert("选择数据时间")
            return
        }
        $.get(
            "/send_me/",
            {
                "id": row["_id"],
                "date": $("#date").val()
            },
            function (data) {
                if (data["errmsg"]) {
                    alert(data["errmsg"])
                    return;
                }
                alert(JSON.stringify(data))
            }
        )
    }
};
window.previewEvents = {
    'click .preview': function (e, value, row, index) {
        if ($("#date").val() === "") {
            alert("选择数据时间")
            return
        }
        $.get(
            "/message_str/",
            {
                "id": row["_id"],
                "date": $("#date").val()
            },
            function (data) {
                if (data["errmsg"]) {
                    alert(data["errmsg"])
                    return;
                }
                alert(data["message"])
            }
        )
    }
}
window.send_othersEvents = {
    'click .send_others': function (e, value, row, index) {
        if ($("#date").val() === "") {
            alert("选择数据时间")
            return
        }
        $.get(
            "/send_others/",
            {
                "id": row["_id"],
                "date": $("#date").val()
            },
            function (data) {
                if (data["errmsg"]) {
                    alert(data["errmsg"])
                    return;
                }
                alert("无errmsg")
            }
        )
    }
};
$("#productBtn").on("click", function (e) {
    $("#productList").bootstrapTable()
    $("#productList").bootstrapTable("refresh", {"silent": true})
    $("#productModal").modal("show");
});
$("#addProduct").on("click", function (e) {
    $("#productList").bootstrapTable("append", {"_id": "", "name": "", "run_time": ""})
})
$("#productList").on('editable-save.bs.table', function (e, field, row, old, $el) {
    if (row["name"] === "") {
        alert("产品名不能为空")
        row[field] = old
        e.destroy()
        return;
    }
    var data = {};
    if (row["_id"] !== "") {
        data["_id"] = row["_id"];
    }
    data[field] = $.trim(row[field]);
    $.post("/product/",
        data,
        function (data, textStatus, jqXHR) {
            if (data["errmsg"]) {
                alert(data["errmsg"])
                return;
            }
            $("#productList").bootstrapTable("refresh", {"silent": true})
            // alert(JSON.stringify(data))
        },
        "json")
    e.stopPropagation();
});

function loadApps() {
    $.get(
        "/product_list/",
        {},
        function (data) {
            if (data["errmsg"]) {
                alert(data["errmsg"])
                return;
            }
            select = $("#messageApp");
            select.empty();
            for (i = 0; i < data.length; ++i) {
                group = data[i];
                select.append("<option>" + group["name"] + "</option>");
            }
        }
    )
}

//新建消息
$add.on('click', function (e) {
    $("#messageName").val("");
    $("#messageApp").val("");
    $("#messageModule").val("");
    $("#messageDesc").val("");
    // $("#peopleList").val("");
    initPeopleTable();
    $peopleTable.bootstrapTable("removeAll");
    loadPeopleList("");
    //新联系人
    $("#group_name").val("");
    loadApps()
    $("#newMessageModal").modal("show");
    $("#editMessageSave").hide();
    $("#newMessageSave").show();
});
window.modifyNormEvents = {
    //修改指标事件
    'click .edit': function (e, value, row, index) {
        body = $("#newNormModal")
        input_fields = $(body.find("input"));
        for (var i = 0; i < input_fields.length; ++i) {
            field = $(input_fields[i]);
            field.val(row[field.attr("id")]);
        }
        select_fields = $(body.find("select"));
        for (var i = 0; i < select_fields.length; ++i) {
            field = $(select_fields[i]);
            field.val(row[field.attr("id")]);
        }
        $("#newNormModal").modal("show");
        $("#editNormSave").show();
        $("#newNormSave").hide();
        var parentid = $(this).parent().parent().parent().parent().data("parentid");
        // alert(parentid);
        $("#editNormSave").data("parentid", parentid);
        $("#editNormSave").data("index", index);
        $("#editNormSave").unbind();
        $("#editNormSave").on('click', function (e) {
            // alert("editNormSave");
            data = {"_id": row["_id"]};
            body = $("#newNormModal")
            input_fields = $(body.find("input"));
            for (var i = 0; i < input_fields.length; ++i) {
                field = $(input_fields[i]);
                data[field.attr("id")] = field.val();
            }
            select_fields = $(body.find("select"));
            for (var i = 0; i < select_fields.length; ++i) {
                field = $(select_fields[i]);
                data[field.attr("id")] = field.val();
            }
            data["belong_message"] = $("#editNormSave").data("parentid");
            // alert($("#editNormSave").data("parentid"));
            data["_id"] = row["_id"];
            // alert(JSON.stringify(data));
            $.post(
                "/norm/",
                data,
                function (data, textStatus, jqXHR) {
                    if (data["errmsg"]) {
                        alert(data["errmsg"])
                        return;
                    }
                    for (k in data) {
                        row[k] = data[k];
                    }
                    $("#sub_" + $("#editNormSave").data("parentid")).bootstrapTable("updateRow", {
                        "index": index,
                        "row": row
                    });
                }
            )
        });
        e.stopPropagation();

    },
    'click .remove': function (e, value, row, index) {
        this_table = $("#sub_" + row["belong_message"]);
        $.post(
            "/norm_delete/",
            {
                "_id": row["_id"]
            },
            function (data, textStatus, jqXHR) {
                if (data["errmsg"]) {
                    alert(data["errmsg"])
                    return;
                }
                $(this_table).bootstrapTable("removeByUniqueId", row["_id"]);
            }
        );
        //alert("removesub");
        e.stopPropagation();
    }
}
//删除联系人事件
window.deletePeopleEvents = {
    'click .remove': function (e, value, row, index) {
        $peopleTable.bootstrapTable("remove", {field: 'name', values: [row["name"]]});
        e.stopPropagation();
    }
}

//修改消息保存
$("#editMessageSave").on("click", function (e) {
    var people = {};
    var people_list = $peopleTable.bootstrapTable("getData");
    for (var x = 0; x < people_list.length; ++x) {
        if ($.trim(people_list[x]["name"]) !== "" && $.trim(people_list[x]["phone"]) !== "") {
            people[people_list[x]["name"]] = people_list[x]["phone"];
        }
    }
    row = $("#newMessageModal").data("row")
    index = $("#newMessageModal").data("index")
    // alert(people["one"]);
    // alert(JSON.stringify(people))
    $.post(
        "/message/",
        {
            "_id": row["_id"],
            "name": $("#messageName").val(),
            "app": $("#messageApp").val(),
            "module": $("#messageModule").val(),
            "desc": $("#messageDesc").val(),
            "people_list": JSON.stringify(people)
        },
        function (data, textStatus, jqXHR) {
            if (data["errmsg"]) {
                alert(data["errmsg"])
                return;
            }

            for (k in data) {
                row[k] = data[k];
            }
            $table.bootstrapTable("updateRow", {"index": index, "row": row});
        }
    )
});
//新建消息保存
$("#newMessageSave").on("click", function (e) {
    var people = {};
    var people_list = $peopleTable.bootstrapTable("getData");
    for (var x = 0; x < people_list.length; ++x) {
        if ($.trim(people_list[x]["name"]) !== "" && $.trim(people_list[x]["phone"]) !== "") {
            people[people_list[x]["name"]] = people_list[x]["phone"];
        }
    }
    $.post(
        "/message/",
        {
            "name": $("#messageName").val(),
            "app": $("#messageApp").val(),
            "module": $("#messageModule").val(),
            "desc": $("#messageDesc").val(),
            "people_list": JSON.stringify(people)
        },
        function (data, textStatus, jqXHR) {
            if (data["errmsg"]) {
                alert(data["errmsg"])
                return;
            }
            $table.bootstrapTable("prepend", data);
        }
    )
});

function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

$(function () {
    var scripts = [location.search.substring(1)
        || '/static/js/bootstrap-table.js',
            '/static/js/bootstrap-table-export.js',
            // 'http://rawgit.com/hhurz/tableExport.jquery.plugin/master/tableExport.js',
            '/static/js/bootstrap-table-editable.js',
            // 'http://rawgit.com/vitalets/x-editable/master/dist/bootstrap3-editable/js/bootstrap-editable.js'
        ],
        eachSeries = function (arr, iterator, callback) {
            callback = callback || function () {
            };
            if (!arr.length) {
                return callback();
            }
            var completed = 0;
            var iterate = function () {
                iterator(arr[completed], function (err) {
                    if (err) {
                        callback(err);
                        callback = function () {
                        };
                    }
                    else {
                        completed += 1;
                        if (completed >= arr.length) {
                            callback(null);
                        }
                        else {
                            iterate();
                        }
                    }
                });
            };
            iterate();
        };

    eachSeries(scripts, getScript, initTable);
});

function getScript(url, callback) {
    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.src = url;

    var done = false;
    // Attach handlers for all browsers
    script.onload = script.onreadystatechange = function () {
        if (!done && (!this.readyState ||
                this.readyState == 'loaded' || this.readyState == 'complete')) {
            done = true;
            if (callback)
                callback();

            // Handle memory leak in IE
            script.onload = script.onreadystatechange = null;
        }
    };

    head.appendChild(script);

    // We handle everything using the script element injection
    return undefined;
}

function addPeople(e) {
    $peopleTable.bootstrapTable("append", ({"name": "", "phone": ""}))
}

$("#new_group").on('click', function (e) {
    var people = {};
    var people_list = $peopleTable.bootstrapTable("getData");
    for (var x = 0; x < people_list.length; ++x) {
        if ($.trim(people_list[x]["name"]) !== "" && $.trim(people_list[x]["phone"]) !== "") {
            people[people_list[x]["name"]] = people_list[x]["phone"];
        }
    }
    $.post(
        "/people_group/",
        {
            "group_name": $("#group_name").val(),
            "people_list": JSON.stringify(people)
        },
        function (data, textStatus, jqXHR) {
            if (data["errmsg"]) {
                alert(data["errmsg"])
                return;
            }
            loadPeopleList($("#group_name").val());
            $("#group_name").val("");
        }
    )
    //保存新联系人组
})
$("#group").on("change", function (e) {
    people_list = $(this).children('option:selected').data("people_list");
    var people = [];
    for (k in people_list) {
        people.push({"name": k, "phone": people_list[k]});
    }
    $peopleTable.bootstrapTable("load", people);

})
