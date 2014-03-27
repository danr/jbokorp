/* lemma => grundform, base form
 * lexem => lemgram, lemgram
 *
 */
var settings = {};

var isLab = window.isLab || false;

settings.lemgramSelect = true;
settings.autocomplete = true;

// for extended search dropdown, can be 'union' or 'intersection'
settings.word_attribute_selector = "union"
settings.struct_attribute_selector = "union"

// for 'compile statistics by' selector, can be 'union' or 'intersection'
settings.reduce_word_attribute_selector = "union"
settings.reduce_struct_attribute_selector = "intersection"


settings.wordpictureTagset = {
    // supported pos-tags
    verb : "vb",
    noun : "nn",
    adjective : "jj",
    adverb : "ab",
    preposition : "pp",

    // dependency releations
    subject : "ss",
    object : "obj",
    adverbial : "adv",
    preposition_rel : "pa",
    pre_modifier : "at",
    post_modifier : "et"

}


settings.wordPictureConf = {
    verb : [[
        {rel : "subject", css_class : "color_blue"},
        "_",
        {rel : "object", css_class : "color_purple"},
        {rel : "adverbial", css_class : "color_green"}
    ]],
    noun : [
        [{rel : "preposition_rel", css_class : "color_yellow", field_reverse: true},
         {rel : "pre_modifier", css_class : "color_azure"},
         "_",
         {rel : "post_modifier", css_class : "color_red"}],

        ["_", {rel : "subject", css_class : "color_blue", field_reverse: true, alt_label : "vb"}],
        [{rel : "object", css_class : "color_purple", field_reverse: true, alt_label : "vb"}, "_"]
    ],
    adjective : [["_", {rel: "pre_modifier", css_class : "color_yellow", field_reverse : true}]],
    adverb : [["_", {rel: "adverbial", css_class : "color_yellow", field_reverse : true}]],
    preposition : [["_", {rel: "preposition_rel", css_class : "color_green"}]]

}

settings.visibleModes = 6
settings.modeConfig = [
    {
        localekey: "modern_texts",
        mode: "default"
    },
    {
        localekey: "parallel_texts",
        mode: "parallel"
    },
    {
        localekey: "old_swedish_texts",
        mode: "old_swedish"
    },
    {
        localekey: "lb_texts",
        mode: "lb"
    },
    {
        localekey: "kubhist",
        mode: "kubhist"
    },
    {
        localekey: "all_hist",
        mode: "all_hist",
    },
    {
        localekey: "spf_texts",
        mode: "spf"
    },
    {
        localekey: "fisk1800_texts",
        mode: "fisk1800"
    },
    {
        localekey: "faroese_texts",
        mode: "faroe"
    },
    {
        localekey: "siberian_texts",
        mode: "siberian_german",
    },
    {
        localekey: "kioping_texts",
        mode: "kioping_books",
    },
    {
        localekey: "runeberg",
        mode: "runeberg",
    },

    {
        localekey: "1800_texts",
        mode: "1800",
    },
    {
        localekey: "lawroom",
        mode: "law",
    }

];

settings.languages = ["sv", "en"];


var karpLemgramLink = "http://spraakbanken.gu.se/karp/#search=cql%7C(lemgram+%3D+%22<%= val.replace(/:\\d+/, '') %>%22)+sortBy+lemgram";

settings.primaryColor = "rgb(221, 233, 255)";
settings.primaryLight = "rgb(242, 247, 255)";
settings.secondaryColor = "";
settings.corpora = {};
settings.defaultContext = {
    "1 sentence" : "1 sentence"
};
settings.spContext = {
    "1 sentence" : "1 sentence",
    "1 paragraph" : "1 paragraph"
};
settings.defaultWithin = {
    "sentence" : "sentence"
};
settings.spWithin = {
    "sentence" : "sentence",
    "paragraph" : "paragraph"
};

settings.defaultLanguage = "sv";

/*
 * ATTRIBUTES
 */
// for optimization purposes
settings.cqp_prio = ['deprel', 'pos', 'msd', 'suffix', 'prefix', 'grundform', 'lemgram', 'saldo', 'word'];


settings.defaultOptions = {
    "is" : "=",
    "is_not" : "!=",
    "starts_with" : "^=",
    "contains" : "_=",
    "ends_with" : "&=",
    "matches" : "*=",
}
settings.liteOptions = {
    "is" : "=",
    "is_not" : "!="
}
settings.setOptions = {
    "is" : "contains",
    "is_not" : "not contains"
}


// settings.getTransformFunc = function(type, value, opt) {

//  if(type == "word" && !value) return function() {return "";};

//  if(type == "date_interval") {
//      c.log("date_interval", arguments)
//      var from = value[0].toString() + "0101";
//      var to = value[1].toString() + "1231";

//      var operator1 = ">=", operator2 = "<=", bool = "&";
//      if(opt == "is_not") {
//          operator1 = "<";
//          operator2 = ">";
//          bool = "|";
//      }

//      return function() {
//          return $.format("(int(_.text_datefrom) %s %s %s int(_.text_dateto) %s %s)",
//                  [operator1, from, bool, operator2, to]);
//      };

//  }
// };

// settings.liteOptions = $.exclude(settings.defaultOptions, ["starts_with", "contains", "ends_with", "matches"]);
// settings.liteOptions = _.omit.apply(null, [settings.defaultOptions, "starts_with", "contains", "ends_with", "matches"]);


var selectType = {
    extended_template : "<select ng-model='model' "
     + "ng-options='tuple[0] as localize(tuple[1]) for tuple in dataset' ></select>",
    controller : function($scope) {
        $scope.localize = function(str) {
            if($scope.localize === false) {
                return str;
            } else {
                return util.getLocaleString( ($scope.translationKey || "") + str);
            }
        }

        $scope.translationKey = $scope.translationKey || "";
        var dataset;
        if(_.isArray($scope.dataset)) {
            // convert array datasets into objects
            dataset = _.object(_.map($scope.dataset, function(item) {
                return [item, item];
            }));
        }
        $scope.dataset = dataset || $scope.dataset;

        $scope.dataset = _.sortBy(_.pairs($scope.dataset), function(tuple) {
            return $scope.localize(tuple[1]);
        });
        $scope.model = $scope.model || $scope.dataset[0][0]
    }
}

var attrs = {};  // positional attributes
var sattrs = {}; // structural attributes

attrs.trans = {
    label : "trans"
}

attrs.tags = {
    label : "tags"
}

attrs.pos = {
    label : "pos",
    displayType : "select",
    opts : settings.liteOptions,
    extended_template : selectType.extended_template,
    controller : selectType.controller,


};
attrs.msd = {
    label : "msd",
    opts : settings.defaultOptions,
    extended_template : '<input class="arg_value" ng-model="model">' +
    '<span ng-click="onIconClick()" class="ui-icon ui-icon-info"></span>',
    controller : function($scope, $modal) {


        var modal = null;

        $scope.onIconClick = function() {
            modal = $modal.open({
                template : '<div>' +
                                '<div class="modal-header">' +
                                    '<h4>{{\'msd_long\' | loc}}</h4>' +
                                '</div>' +
                                '<div ng-click="msdClick($event)" ng-include="\'markup/msd.html\'"></div>' +
                            '</div>',
                scope : $scope
            })
        }
        $scope.msdClick = function(event) {
            c.log(event, arguments)
            val = $(event.target).parent().data("value")
            $scope.model = val
            modal.close();
        }
    }
};
attrs.baseform = {
    label : "baseform",
    type : "set",
    displayType : "autocomplete",
    stringify : function(baseform) {
        return baseform.replace(/:\d+$/,'').replace(/_/g,' ');
    },
    opts : settings.setOptions,
    extended_template : "<input korp-autocomplete model='model' stringify='stringify' sorter='sorter' type='baseform' >",
    controller : function($scope) {
        $scope.stringify = util.lemgramToString;
        $scope.sorter = view.lemgramSort;
    }

};
attrs.lemgram = {
    label : "lemgram",
    type : "set",
    displayType : "autocomplete",
    opts : settings.setOptions,
    stringify : function(lemgram) {
        // if(_.contains(lemgram, " "))
        // TODO: what if we're getting more than one consequtive lemgram back?
        return util.lemgramToString(_.str.trim(lemgram), true);
    },
    externalSearch : karpLemgramLink,
    internalSearch : true,
    extended_template : "<input korp-autocomplete model='model' stringify='stringify' sorter='sorter' type='lem' >",
    controller : function($scope) {
        $scope.stringify = util.lemgramToString;
        $scope.sorter = view.lemgramSort;
    }
};
attrs.saldo = {
    label : "saldo",
    type : "set",
    displayType : "autocomplete",
    opts : settings.setOptions,
    stringify : function(saldo) {
        return util.saldoToString(saldo, true);
    },
    externalSearch : "http://spraakbanken.gu.se/karp/#search-tab-1&search=cql|(saldo+%3D+<%= val %>)",
    internalSearch : true,
    extended_template : "<input korp-autocomplete model='model' stringify='stringify' sorter='sorter' type='saldo' >",
    controller : function($scope) {
        $scope.stringify = util.saldoToString;
        $scope.sorter = view.saldoSort;
    }
};
attrs.dephead = {
    label : "dephead",
    displayType : "hidden"
};
attrs.deprel = {
    label : "deprel",
    displayType : "select",
    translationKey : "deprel_",
    extended_template : selectType.extended_template,
    controller : selectType.controller,
    dataset : {
        "++" : "++",
        "+A" : "+A",
        "+F" : "+F",
        "AA" : "AA",
        "AG" : "AG",
        "AN" : "AN",
        "AT" : "AT",
        "CA" : "CA",
        "DB" : "DB",
        "DT" : "DT",
        "EF" : "EF",
        "EO" : "EO",
        "ES" : "ES",
        "ET" : "ET",
        "FO" : "FO",
        "FP" : "FP",
        "FS" : "FS",
        "FV" : "FV",
        "I?" : "I?",
        "IC" : "IC",
        "IG" : "IG",
        "IK" : "IK",
        "IM" : "IM",
        "IO" : "IO",
        "IP" : "IP",
        "IQ" : "IQ",
        "IR" : "IR",
        "IS" : "IS",
        "IT" : "IT",
        "IU" : "IU",
        "IV" : "IV",
        "JC" : "JC",
        "JG" : "JG",
        "JR" : "JR",
        "JT" : "JT",
        "KA" : "KA",
        "MA" : "MA",
        "MS" : "MS",
        "NA" : "NA",
        "OA" : "OA",
        "OO" : "OO",
        "OP" : "OP",
        "PL" : "PL",
        "PR" : "PR",
        "PT" : "PT",
        "RA" : "RA",
        "SP" : "SP",
        "SS" : "SS",
        "TA" : "TA",
        "TT" : "TT",
        "UK" : "UK",
        "VA" : "VA",
        "VO" : "VO",
        "VS" : "VS",
        "XA" : "XA",
        "XF" : "XF",
        "XT" : "XT",
        "XX" : "XX",
        "YY" : "YY",
        "CJ" : "CJ",
        "HD" : "HD",
        "IF" : "IF",
        "PA" : "PA",
        "UA" : "UA",
        "VG" : "VG"
    },
    opts : settings.liteOptions
};
attrs.prefix = {
    label : "prefix",
    type : "set",
    displayType : "autocomplete",
    opts : settings.setOptions,
    stringify : function(lemgram) {
        return util.lemgramToString(lemgram, true);
    },
    externalSearch : karpLemgramLink,
    internalSearch : true,
    extended_template : "<input korp-autocomplete model='model' stringify='stringify' sorter='sorter' type='lem' >",
    controller : function($scope) {
        $scope.stringify = util.lemgramToString;
        $scope.sorter = view.lemgramSort;
    }
};
attrs.suffix = {
    label : "suffix",
    type : "set",
    displayType : "autocomplete",
    opts : settings.setOptions,
    stringify : function(lemgram) {
        return util.lemgramToString(lemgram, true);
    },
    externalSearch : karpLemgramLink,
    internalSearch : true,
    extended_template : "<input korp-autocomplete model='model' stringify='stringify' sorter='sorter' type='lem' >",
    controller : function($scope) {
        $scope.stringify = util.lemgramToString;
        $scope.sorter = view.lemgramSort;
    }
};
attrs.ref = {
    label : "ref",
    displayType : "hidden"
};
attrs.link = {
    label : "sentence_link"
};
sattrs.date = {
    label : "date",
    displayType : "date"
};

settings.common_struct_types = {
    date_interval : {
        label: "date_interval",
        displayType: "date_interval",

        opts: settings.liteOptions,
        extended_template : '<slider floor="{{floor}}" ceiling="{{ceiling}}" ' +
                                'ng-model-low="values.low" ng-model-high="values.high"></slider>' +
                                '<div><input ng-model="values.low" class="from"> <input class="to" ng-model="values.high"></div>',
        controller : function($scope, searches, $timeout) {
            c.log( "searches", searches)
            var s = $scope

            searches.timeDef.then(function() {
                var all_years = _(settings.corpusListing.selected)
                            .pluck("time")
                            .map(_.pairs)
                            .flatten(true)
                            .filter(function(tuple) {
                                return tuple[0] && tuple[1];
                            }).map(_.compose(Number, _.head))
                            .value();

                s.values = {}

                $timeout(function() {
                    s.floor = Math.min.apply(null, all_years)
                    s.ceiling = Math.max.apply(null, all_years)
                    if(!s.model) {
                        s.values.low = s.floor;
                        s.values.high = s.ceiling;
                    } else {
                        s.values.low = s.model.split(",")[0].slice(0, 4);
                        s.values.high = s.model.split(",")[1].slice(0, 4);
                    }
                }, 0)
                w = s.$watch("values.low.toString() + values.high.toString()", function() {
                    // TODO: seems to be be running too much
                    c.log ("low", s.values.low, "high", s.values.high, s.floor, s.ceiling)
                    if(!angular.isDefined(s.values.low) || isNaN(s.values.low) || isNaN(s.values.high) || !angular.isDefined(s.values.high)) {
                        s.model = ""
                        return
                    }

                    // s.model = s.values.low.toString() + s.values.high.toString()
                    s.model = [
                        s.values.low.toString() + "0101",
                        s.values.high.toString() + "1231"
                    ].join(",")
                })

                s.$on("$destroy", function() {
                    w();
                })

            })

        }
    }

}

var modernAttrs = {
    pos : attrs.pos,
    msd : attrs.msd,
    lemma : attrs.baseform,
    lex : attrs.lemgram,
    saldo : attrs.saldo,
    dephead : attrs.dephead,
    deprel : attrs.deprel,
    ref : attrs.ref,
    prefix : attrs.prefix,
    suffix : attrs.suffix
};

/*
 * FOLDERS
 */

settings.corporafolders = {};

settings.corporafolders.korpora = {
    title : "korpora",
    contents : ["ca_pa_djedi"]
};



/*
 * CORPORA
 */

settings.corpora.ca_pa_djedi = {
    title : "korpora",
    id : "ca_pa_djedi",
    description : "",
    within : settings.spWithin,
    context : settings.spContext,
    attributes : {
        pos: attrs.pos,
        tags: attrs.tags,
        trans: attrs.trans,
        dephead: attrs.dephead,
        deprel: attrs.deprel
    },
    struct_attributes : {
    }
};



/*
 * MISC
 */

settings.cgi_script = "http://localhost:9999/cgi/korp.cgi";
// settings.cgi_script = "http://spraakbanken.gu.se/ws/korp";
// settings.cgi_script = "http://demosb.spraakdata.gu.se/cgi-bin/korp/korp2.cgi";
// settings.cgi_script = "http://spraakbanken.gu.se/ws/korp";
// settings.cgi_script = "http://demosb.spraakdata.gu.se/cgi-bin/korp/korp_sme.cgi";
// settings.cgi_script = "http://demosb.spraakdata.gu.se/cgi-bin/korp/korp2.cgi";

// label values here represent translation keys.
settings.arg_groups = {
    "word" : {
        word : {label : "word"}
    }
};


settings.reduce_stringify = function(type) {
    function filterCorpora(rowObj) {
        return $.grepObj(rowObj, function(value, key) {
            return key != "total_value" && $.isPlainObject(value);
        });
    }

    function getCorpora(dataContext) {
        var corpora = $.grepObj(filterCorpora(dataContext), function(value, key) {
            return value.relative != null;
        });
        corpora = $.map($.keys(corpora), function(item) {
            return item.split("_")[0].toLowerCase();
        });
        return corpora;
    }

    function appendDiagram(output, corpora, value) {
        //if(corpora.length > 1)
            return output + $.format('<img id="circlediagrambutton__%s" src="img/stats2.png" class="arcDiagramPicture"/>', value);
        //else
        //    return output;
    }
    var output = "";
    switch(type) {
    case "word":
        return function(row, cell, value, columnDef, dataContext) {
            var corpora = getCorpora(dataContext);
            if(value == "&Sigma;") return appendDiagram(value, corpora, value);

            var query = $.map(dataContext.hit_value.split(" "), function(item) {
                return $.format('[word="%s"]', item);
            }).join(" ");

            output = $("<span>",
                    {
                    "class" : "link",
                    "data-query" : encodeURIComponent(query),
                    "data-corpora" : JSON.stringify(corpora)
                    }).text(value).outerHTML();
            return appendDiagram(output, corpora, value);

        };

    case "pos":
        return function(row, cell, value, columnDef, dataContext) {
            var corpora = getCorpora(dataContext);
            if(value == "&Sigma;") return appendDiagram(value, corpora, value);
            var query = $.map(dataContext.hit_value.split(" "), function(item) {
                return $.format('[pos="%s"]', item);
            }).join(" ");
            output =  _.map(value.split(" "), function(token) {
                return $("<span>")
                .localeKey("pos_" + token)
                .outerHTML()
            })
            var link = $("<span>").addClass("link")
                .attr("data-query", query)
                .attr("data-corpora", JSON.stringify(corpora))
                .html(output.join(" "))
            return appendDiagram(link.outerHTML(), corpora, value);
        };
    case "prefix":
    case "suffix":
    case "lex":
        return function(row, cell, value, columnDef, dataContext) {
        var corpora = getCorpora(dataContext);
        if(value == "&Sigma;") return appendDiagram(value, corpora, value);
        // else if(value == "|") return "-";
        output = _.map(value.split(" "), function(token) {
            if(token == "|") return "–";
            return _(token.split("|"))
                    .filter(Boolean)
                    .map(function(item) {
                        var wrapper = $("<div>");
                        $("<span>").html(util.lemgramToString(item, true)).attr("data-cqp", '[lex contains "' + item + '"]').appendTo(wrapper);
                        return wrapper.html();
                    })
                    .join(", ");

        });
        return appendDiagram(output.join(" "), corpora, value);
        };
    case "saldo":
        return function(row, cell, value, columnDef, dataContext) {
        var corpora = getCorpora(dataContext);
        if(value == "&Sigma;") return appendDiagram(value, corpora, value);
        else if(value == "|") return "-";
        output = _(value.split("|"))
                .filter(Boolean)
                .map(function(item) {
                    return util.saldoToString(item, true);
                })
                .join(", ");
        return appendDiagram(output, corpora, value);
        };
    case "deprel":
        return function(row, cell, value, columnDef, dataContext) {
            var corpora = getCorpora(dataContext);
            if(value == "&Sigma;") return appendDiagram(value, corpora, value);
            var query = $.map(dataContext.hit_value.split(" "), function(item) {
                return $.format('[deprel="%s"]', item);
            }).join(" ");
            output = $.format("<span class='link' data-query='%s' data-corpora='%s' rel='localize[%s]'>%s</span> ",
                    [query, JSON.stringify(corpora),"deprel_" + value, util.getLocaleString("deprel_" + value)]);
            return appendDiagram(output, corpora, value);

        };
    default:
        return function(row, cell, value, columnDef, dataContext) {
            var corpora = getCorpora(dataContext);
            var query = $.map(dataContext.hit_value.split(" "), function(item) {
                return $.format('[%s="%s"]', [value, item]);
            }).join(" ");
            output = $.format("<span data-query='%s' data-corpora='%s' rel='localize[%s]'>%s</span> ",
                    [query, JSON.stringify(corpora),"deprel_" + value, util.getLocaleString(value)]);
            if(value == "&Sigma;") return appendDiagram(output, corpora, value);

            return appendDiagram(output, corpora, value);
        };
    }

    return output;
};


delete attrs;
delete sattrs;
delete context;
delete ref;




settings.posset = {
   type : "set",
   label : "pos",
   displayType : "select",
   opts : settings.setOptions,
   translationKey : "pos_",
   extended_template : selectType.extended_template,
   controller : selectType.controller,
   dataset :  {
    "AB" : "AB",
    "MID|MAD|PAD" : "DL",
    "DT" : "DT",
    "HA" : "HA",
    "HD" : "HD",
    "HP" : "HP",
    "HS" : "HS",
    "IE" : "IE",
    "IN" : "IN",
    "JJ" : "JJ",
    "KN" : "KN",
    "NN" : "NN",
    "PC" : "PC",
    "PL" : "PL",
    "PM" : "PM",
    "PN" : "PN",
    "PP" : "PP",
    "PS" : "PS",
    "RG" : "RG",
    "RO" : "RO",
    "SN" : "SN",
    "UO" : "UO",
    "VB" : "VB"
            }
};
settings.fsvlemma = {
    //pattern : "<a href='http://spraakbanken.gu.se/karp/#search=cql%7C(gf+%3D+%22<%= key %>%22)+sortBy+wf'><%= val %></a>",
    type : "set",
    label : "baseform",
    displayType : "autocomplete",
    opts : settings.setOptions,
    stringify : function(baseform) {
        return baseform.replace(/:\d+$/,'').replace(/_/g,' ');
    }
//      externalSearch : "http://spraakbanken.gu.se/karp/#search=cql%7C(gf+%3D+%22<%= val %>%22)+sortBy+lemgram",
//  internalSearch : true

};
settings.fsvlex = {
    type : "set",
    label : "lemgram",
    displayType : "autocomplete",
    opts : settings.setOptions,
    stringify : function(str) {
        return util.lemgramToString(str, true);
    },
    externalSearch : karpLemgramLink,
    internalSearch : true
};
settings.fsvvariants = {
    type : "set",
    label : "variants",
    stringify : function(str) {
        return util.lemgramToString(str, true);
    },
    displayType : "autocomplete",
    opts : settings.setOptions,
    externalSearch : karpLemgramLink,
    internalSearch : true
};

settings.fsvdescription ='<a href="http://project2.sol.lu.se/fornsvenska/">Fornsvenska textbanken</a> är ett projekt som digitaliserar fornsvenska texter och gör dem tillgängliga över webben. Projektet leds av Lars-Olof Delsing vid Lunds universitet.';
var fsv_yngrelagar = {
    morf : 'fsvm',
    id : "fsv-yngrelagar",
    title : "Yngre lagar – Fornsvenska textbankens material",
    description : settings.fsvdescription,
    within : settings.defaultWithin,
    context : settings.spContext,
    attributes : {
        posset : settings.posset,
        lemma : settings.fsvlemma,
        lex : settings.fsvlex,
        variants : settings.fsvvariants
        },
    struct_attributes : {
        text_title : {
            label : "title",
            displayType : "select",
            localize : false,
            extended_template : selectType.extended_template,
            controller : selectType.controller,
            dataset : [
                "Kristoffers Landslag, nyskrivna flockar i förhållande till MEL",
                "Kristoffers Landslag, innehållsligt ändrade flockar i förhållande til MEL",
                "Kristoffers Landslag, flockar direkt hämtade från MEL",
                "Kristoffers Landslag"
                ],
        },
        text_date : {label : "date"}
    }
};

var fsv_aldrelagar = {
    morf : 'fsvm',
    id : "fsv-aldrelagar",
    title : "Äldre lagar – Fornsvenska textbankens material",
    description : settings.fsvdescription,
    within : settings.defaultWithin,
    context : settings.spContext,
    attributes : {
        posset : settings.posset,
        lemma : settings.fsvlemma,
        lex : settings.fsvlex,
        variants : settings.fsvvariants
                },
    struct_attributes : {
        text_title : {
            label : "title",
            displayType : "select",
            localize : false,
            extended_template : selectType.extended_template,
            controller : selectType.controller,
            dataset : [
                "Yngre Västgötalagens äldsta fragment, Lydekini excerpter och anteckningar",
                "Tillägg till Upplandslagen, hskr A (Ups B 12)",
                "Södermannalagen, enligt Codex iuris Sudermannici",
                "Östgötalagen, fragment H, ur Kyrkobalken ur Skokloster Avdl I 145",
                "Yngre Västmannalagen, enl Holm B 57",
                "Vidhemsprästens anteckningar",
                "Magnus Erikssons Stadslag, exklusiva stadslagsflockar",
                "Södermannalagens additamenta, efter NKS 2237",
                "Hälsingelagen",
                "Yngre Västgötalagen, tillägg, enligt Holm B 58",
                "Östgötalagen, fragment C, ur Holm B 1709",
                "Yngre Västgötalagen, enligt Holm B 58",
                "Upplandslagen enl Schlyters utgåva och Codex Ups C 12, hskr A",
                "Skånelagen, enligt Holm B 76",
                "Östgötalagen, fragment D, ur Holm B 24",
                "Östgötalagen A, ur Holm B 50",
                "Äldre Västgötalagen",
                "Östgötalagen, fragment M, ur Holm B 196",
                "Gutalagen enligt Holm B 64",
                "Upplandslagen enligt Codex Holm B 199, Schlyters hskr B",
                "Smålandslagens kyrkobalk",
                "Dalalagen (Äldre Västmannalagen)",
                "Gutalagens additamenta enligt AM 54",
                "Bjärköarätten",
                "Magnus Erikssons Landslag",
                "Östgötalagen, fragment N, ur Köpenhamn AM 1056",
                "Södermannalagen stadsfästelse - Confirmatio, enligt NKS 2237",
                "Östgötalagen, fragment E, ur Ups B 22"
                            ],
        },
        text_date : {label : "date"}
    }
};




