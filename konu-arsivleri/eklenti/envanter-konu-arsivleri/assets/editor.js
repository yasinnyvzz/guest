/* Envanter Konu Arşivleri — editör öneri kutusu (bağımlılık: wp-api-fetch). */
( function () {
	'use strict';
	var box = document.getElementById( 'eka-box' );
	if ( ! box ) {
		return;
	}
	var postId = parseInt( box.getAttribute( 'data-post' ), 10 );
	var out = document.getElementById( 'eka-sonuc' );
	var etiket = { yuksek: 'Yüksek', orta: 'Orta', dusuk: 'Zayıf' };

	function editorStore() {
		return window.wp && wp.data && wp.data.select( 'core/editor' ) && wp.data.select( 'core/editor' ).getCurrentPostId ? wp.data : null;
	}

	function current() {
		var d = editorStore();
		if ( d ) {
			var s = d.select( 'core/editor' );
			return { title: s.getEditedPostAttribute( 'title' ) || '', excerpt: s.getEditedPostAttribute( 'excerpt' ) || '', content: s.getEditedPostContent() || '' };
		}
		var t = document.getElementById( 'title' ), e = document.getElementById( 'excerpt' ), c = document.getElementById( 'content' );
		var body = ( window.tinymce && tinymce.get( 'content' ) && ! tinymce.get( 'content' ).isHidden() ) ? tinymce.get( 'content' ).getContent() : ( c ? c.value : '' );
		return { title: t ? t.value : '', excerpt: e ? e.value : '', content: body };
	}

	function el( tag, attrs, text ) {
		var n = document.createElement( tag );
		Object.keys( attrs || {} ).forEach( function ( k ) { n.setAttribute( k, attrs[ k ] ); } );
		if ( text ) { n.textContent = text; }
		return n;
	}

	function render( res ) {
		out.innerHTML = '';
		if ( res.uyari ) {
			out.appendChild( el( 'p', { 'class': 'eka-uyari' }, res.uyari ) );
			return;
		}
		if ( ! res.oneriler.length ) {
			out.appendChild( el( 'p', {}, 'Güçlü bir arşiv eşleşmesi bulunamadı.' ) );
			return;
		}
		var ul = el( 'ul', { 'class': 'eka-liste' } );
		res.oneriler.forEach( function ( o, i ) {
			var li = el( 'li', { 'class': 'eka-' + o.guven } );
			var id = 'eka-o-' + i;
			var cb = el( 'input', { type: 'checkbox', id: id } );
			if ( ! o.arsiv ) {
				cb.disabled = true;
			} else if ( o.arsiv.bagli ) {
				cb.checked = true;
				cb.disabled = true;
			} else if ( o.guven === 'yuksek' ) {
				cb.checked = true;
			}
			cb.dataset.tax = o.arsiv ? o.arsiv.tax : '';
			cb.dataset.id = o.arsiv ? o.arsiv.id : '';
			cb.dataset.name = o.arsiv ? o.arsiv.ad : '';
			var lab = el( 'label', { 'for': id } );
			lab.appendChild( cb );
			lab.appendChild( document.createTextNode( ' ' + o.ad ) );
			li.appendChild( lab );
			li.appendChild( el( 'span', { 'class': 'eka-rozet' }, etiket[ o.guven ] ) );
			var info = o.arsiv ? ( o.arsiv.bagli ? 'Zaten bağlı' : 'Arşiv: ' + o.arsiv.ad ) : 'Bu dilde arşivi yok';
			li.appendChild( el( 'small', { title: o.neden }, info ) );
			ul.appendChild( li );
		} );
		out.appendChild( ul );
		var btn = el( 'button', { type: 'button', 'class': 'button button-primary' }, 'Seçilenleri yazıya ekle' );
		btn.addEventListener( 'click', apply );
		out.appendChild( btn );
		out.appendChild( el( 'p', { 'class': 'description' }, 'Terimler yazıyı kaydettiğinizde uygulanır. Zayıf öneriler varsayılan olarak seçili değildir.' ) );
	}

	function apply() {
		var picked = Array.prototype.slice.call( out.querySelectorAll( 'input[type=checkbox]:checked:not(:disabled)' ) );
		var d = editorStore();
		if ( d ) {
			var s = d.select( 'core/editor' );
			var edits = {};
			[ [ 'category', 'categories' ], [ 'post_tag', 'tags' ] ].forEach( function ( p ) {
				var ids = ( s.getEditedPostAttribute( p[ 1 ] ) || [] ).slice();
				picked.forEach( function ( c ) {
					var id = parseInt( c.dataset.id, 10 );
					if ( c.dataset.tax === p[ 0 ] && ids.indexOf( id ) === -1 ) { ids.push( id ); }
				} );
				edits[ p[ 1 ] ] = ids;
			} );
			d.dispatch( 'core/editor' ).editPost( edits );
		} else {
			picked.forEach( function ( c ) {
				if ( c.dataset.tax === 'category' ) {
					var k = document.getElementById( 'in-category-' + c.dataset.id );
					if ( k ) { k.checked = true; }
				} else {
					var ta = document.getElementById( 'tax-input-post_tag' );
					if ( ta ) {
						var list = ta.value ? ta.value.split( ',' ) : [];
						if ( list.map( function ( x ) { return x.trim(); } ).indexOf( c.dataset.name ) === -1 ) { list.push( c.dataset.name ); }
						ta.value = list.join( ',' );
					}
				}
			} );
		}
		picked.forEach( function ( c ) { c.disabled = true; } );
		out.appendChild( el( 'p', { 'class': 'eka-tamam' }, picked.length + ' arşiv eklendi; kaydetmeyi unutmayın.' ) );
	}

	document.getElementById( 'eka-analiz' ).addEventListener( 'click', function () {
		out.textContent = 'Analiz ediliyor…';
		var c = current();
		wp.apiFetch( { path: '/eka/v1/oner', method: 'POST', data: { post_id: postId, title: c.title, excerpt: c.excerpt, content: c.content } } )
			.then( render )
			.catch( function ( e ) { out.textContent = 'Hata: ' + ( e && e.message ? e.message : e ); } );
	} );
}() );
