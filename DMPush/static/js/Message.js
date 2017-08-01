/**
 * Created by gzs10558 on 2017/7/27.
 */
var $table = $('#table'),
    $add = $('#addMessage'),
    $peopleTable = $("#peopleList");

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
                    $peopleTable.bootstrapTable("removeByUniqueId", row["name"]);
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
        '<table class="table table-striped"></table>'
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
                    ;
                },
                "json")
            e.stopPropagation();
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
                ;
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
        '<a class="preview" href="javascript:void(0)" title="Like">',
        '<i class="glyphicon glyphicon-option-horizontal"></i>',
        '</a>  '
    ].join('');
}
function deletePeopleFormatter(value, row, index) {
    return [
        '<a class="remove" href="javascript:void(0)" title="Remove">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}
//修改指标显示内容
function modifyNormFormatter(value, row, index) {
    return [
        '<a class="edit" href="javascript:void(0)" title="Like">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>  ',
        '<a class="remove" href="javascript:void(0)" title="Remove">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}
//操作列显示内容
function operateFormatter(value, row, index) {
    return [
        '<a class="edit" href="javascript:void(0)" title="Like">',
        '<i class="glyphicon glyphicon-pencil"></i>',
        '</a>  ',
        '<a class="remove" href="javascript:void(0)" title="Remove">',
        '<i class="glyphicon glyphicon-remove"></i>',
        '</a>'
    ].join('');
}
//操作列事件响应
window.operateEvents = {
    //修改消息
    'click .edit': function (e, value, row, index) {
        initPeopleTable();
        var people_list = JSON.parse(row["people_list"]);
        var people = [];
        for (k in people_list) {
            people.push({"name": k, "phone": people_list[k]});
        }
        $peopleTable.bootstrapTable("load", people);
        $("#messageName").val(row["name"]);
        $("#messageApp").val(row["app"]);
        $("#messageModule").val(row["module"]);
        $("#messageDesc").val(row["desc"]);
        $("#newMessageModal").data("index", index);
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
                $table.bootstrapTable("removeByUniqueId", row["_id"]);
            }
        );
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
                alert(data["errmsg"])
            }
        )
    }
};
//新建消息
$add.on('click', function (e) {
    $("#messageName").val("");
    $("#messageApp").val("");
    $("#messageModule").val("");
    $("#messageDesc").val("");
    // $("#peopleList").val("");
    initPeopleTable();
    $peopleTable.bootstrapTable("removeAll");
    //新联系人

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
            data = {};
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
                    $("#sub_" + $("#editNormSave").data("parentid")).bootstrapTable("refresh", {silent: true});
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
                $(this_table).bootstrapTable("removeByUniqueId", row["_id"]);
            }
        );
        alert("removesub");
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
    // alert(people["one"]);
    // alert(JSON.stringify(people))
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
            $table.bootstrapTable("refresh", {silent: true});
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
            $table.bootstrapTable("prepend", data);
        }
    )
});

function getHeight() {
    return $(window).height() - $('h1').outerHeight(true);
}

$(function () {
    var scripts = [location.search.substring(1)
        || 'assets/bootstrap-table/src/bootstrap-table.js',
            'assets/bootstrap-table/src/extensions/export/bootstrap-table-export.js',
            // 'http://rawgit.com/hhurz/tableExport.jquery.plugin/master/tableExport.js',
            'assets/bootstrap-table/src/extensions/editable/bootstrap-table-editable.js',
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
